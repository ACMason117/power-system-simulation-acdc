# optimal_tap_position.py
"""
In this file the processing of the power system should be done. Power system can be given in a different test file. 
"""

import json
import pprint
import warnings

import pandas as pd

# import power_grid_model as pgm
import pyarrow as pa
import pyarrow.parquet as pq

with warnings.catch_warnings(action="ignore", category=DeprecationWarning):
    # suppress warning about pyarrow as future required dependency
    from pandas import DataFrame

from power_grid_model import CalculationMethod, CalculationType, PowerGridModel, initialize_array
from power_grid_model.utils import json_deserialize, json_serialize
from power_grid_model.validation import assert_valid_batch_data, assert_valid_input_data
from pyarrow import table


class PowerProfileNotFound(Exception):
    pass


class TimestampMismatch(Exception):
    pass


class LoadIDMismatch(Exception):
    pass


class OptimalTapPosition:

    def __init__(self, grid_data: dict) -> None:
        """Load grid_data in class 'PowerFlow' upon instantiation

        Args:
            grid_data: Power grid input data. Class dict.
            active_power_profile: Active power profile time data. Class pyarrow.table.
            reactive_power_profile: Reactive power profile time data. Class pyarrow.table.
            ev_active_power_profile: Ev active power profile time date. Class pyarrow.table
        """

        assert_valid_input_data(input_data=grid_data, symmetric=True, calculation_type=CalculationType.power_flow)

        self.grid_data = grid_data

        # do not delete the next two lines!!!!
        # self.active_power_profile = active_power_profile
        # self.reactive_power_profile = reactive_power_profile

        self.model = PowerGridModel(self.grid_data)

    def powerflow(
        self,
        active_power_profile1: pd.DataFrame,
        reactive_power_profile1: pd.DataFrame,
        ev_active_power_profile1: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calculate power flow.

        Args:
            active_power_profile: DataFrame with columns ['Timestamp', '8', '9', '10', ...]
            reactive_power_profile: DataFrame with columns ['Timestamp', '8', '9', '10', ...]
            ev_active_power_profile:

        Returns:
            pd.DataFrame: Power flow solution data.
        """
        # check if any power profile is provided
        if active_power_profile1 is None:
            raise PowerProfileNotFound("No active power profile provided.")

        if reactive_power_profile1 is None:
            raise PowerProfileNotFound("No reactive power profile provided.")

        if ev_active_power_profile1 is None:
            raise PowerProfileNotFound("No ev active power profile provided.")

        # check if timestamps are equal in value and lengths
        if (
            (active_power_profile1.index.to_list() != reactive_power_profile1.index.to_list())
            | (reactive_power_profile1.index.to_list() != ev_active_power_profile1.index.to_list())
            | (active_power_profile1.index.to_list() != ev_active_power_profile1.index.to_list())
        ):
            raise TimestampMismatch("Timestamps of active, reactive, ev active power profiles do not match.")

        if (
            (active_power_profile1.columns.to_list() != reactive_power_profile1.columns.to_list())
            | (active_power_profile1.columns.to_list() != ev_active_power_profile1.columns.to_list())
            | (reactive_power_profile1.columns.to_list() != ev_active_power_profile1.columns.to_list())
        ):
            raise LoadIDMismatch("Load IDs in given power profiles do not match")

        load_profile = initialize_array(
            "update",
            "sym_load",
            (
                len(active_power_profile1.index.to_list()),
                len(active_power_profile1.columns.to_list()),
                len(ev_active_power_profile1.columns.to_list()),
            ),
        )

        load_profile["id"] = active_power_profile1.columns.tolist()
        load_profile["p_specified"] = active_power_profile1.values.tolist()
        load_profile["q_specified"] = reactive_power_profile1.values.tolist()

        # Construct the update data
        update_data = {"sym_load": load_profile}

        # Validate batch data
        assert_valid_batch_data(
            input_data=self.grid_data, update_data=update_data, calculation_type=CalculationType.power_flow
        )

        # Run Newton-Raphson power flow
        output_data = self.model.calculate_power_flow(
            update_data=update_data, calculation_method=CalculationMethod.newton_raphson
        )

        return output_data

    def aggregate_voltage_table(self, output_data: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate power flow results into a table with voltage information.

        Args:
            output_data (pd.DataFrame): Output data from power flow calculation.

        Returns:
            pd.DataFrame: Table with voltage information.
        """
        voltage_table = pd.DataFrame(columns=["Timestamp", "u_pu_max", "id_max", "u_pu_min", "id_min"])

        grouped_data = output_data.groupby("Timestamp")

        for timestamp, group in grouped_data:
            max_voltage = group["u_pu"].max()
            min_voltage = group["u_pu"].min()

            # Get the corresponding node IDs for maximum and minimum p.u. voltage
            node_id_max = group.loc[group["u_pu"] == max_voltage, "id"].values[0]
            node_id_min = group.loc[group["u_pu"] == min_voltage, "id"].values[0]

            # Append to voltage table
            voltage_table = voltage_table.append(
                {
                    "Timestamp": timestamp,
                    "u_pu_max": max_voltage,
                    "id_max": node_id_max,
                    "u_pu_min": min_voltage,
                    "id_min": node_id_min,
                },
                ignore_index=True,
            )

        return voltage_table
