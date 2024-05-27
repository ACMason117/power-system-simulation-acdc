# power_flow_processing.py
"""
In this file the processing of the power system should be done. Power system can be given in a different test file. 
"""

import json
import pprint
import warnings

import pandas as pd
import power_grid_model as pgm
import pyarrow as pa
import pyarrow.parquet as pq

with warnings.catch_warnings(action="ignore", category=DeprecationWarning):
    # suppress warning about pyarrow as future required dependency
    from pandas import DataFrame

from power_grid_model import CalculationMethod, CalculationType, PowerGridModel, initialize_array
from power_grid_model.utils import json_deserialize, json_serialize
from power_grid_model.validation import assert_valid_input_data
from pyarrow import table


class ValidationException(Exception):
    """Power grid model input data not valid.

    Args:
        Exception: Raise error if the input data is invalid.
    """


class PowerFlow:

    def __init__(
        self, grid_data: dict = None, active_power_profile: table = None, reactive_power_profile: table = None
    ) -> None:
        """Load grid_data in class 'PowerFlow' upon instantiation

        Args:
            grid_data: Power grid input data. Class dict.
            active_power_profile: Active power profile time data. Class pyarrow.table.
            reactive_power_profile: Reactive power profile time data. Class pyarrow.table.
        """

        assert_valid_input_data(input_data=grid_data, symmetric=True, calculation_type=CalculationType.power_flow)

        self.grid_data = grid_data
        self.active_power_profile = active_power_profile
        self.reactive_power_profile = reactive_power_profile
        self.model = PowerGridModel(self.grid_data)

    def batch_powerflow(self, active_power_profile: pd.DataFrame, reactive_power_profile: pd.DataFrame) -> pd.DataFrame:
        """
        Create a batch update dataset and calculate power flow.

        Args:
            active_power_profile: DataFrame with columns ['Timestamp', '8', '9', '10', ...]
            reactive_power_profile: DataFrame with columns ['Timestamp', '8', '9', '10', ...]

        Returns:
            pd.DataFrame: Power flow solution data.
        """
        # Melt power flow profiles to long format for merging
        active_profile_long = active_power_profile.melt(
            id_vars=["Timestamp"], var_name="load_id", value_name="active_load"
        )
        reactive_profile_long = reactive_power_profile.melt(
            id_vars=["Timestamp"], var_name="load_id", value_name="reactive_load"
        )

        # Merge the two profiles on 'Timestamp' and 'load_id'
        merged_profile = pd.merge(active_profile_long, reactive_profile_long, on=["Timestamp", "load_id"])

        # Initialize an empty load profile
        load_profile = initialize_array("update", "sym_load", (len(merged_profile), 3))

        # Set the attributes for the batch calculation
        load_profile["id"] = merged_profile["load_id"].to_numpy()
        load_profile["p_specified"] = merged_profile["active_load"].to_numpy()
        load_profile["q_specified"] = merged_profile["reactive_load"].to_numpy()

        # Construct the update data
        update_data = {"sym_load": load_profile}

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

    def process_data(self):
        """
        Do the processing of the grid_data here.
        """
        pprint.pprint(json.loads(self.grid_data))
        dataset = json_deserialize(self.grid_data)
        print("components:", dataset.keys())
        print(DataFrame(dataset["node"]))

        model = PowerGridModel(dataset)
        output = model.calculate_power_flow()
        print(DataFrame(output["node"]))

        # serialized_output = json_serialize(output)
        print(serialized_output)

        if self.active_power_profile is not None:
            print("Active Power Profile Data:")
            print(self.active_power_profile)
        else:
            print("No active power profile data provided.")

        if self.reactive_power_profile is not None:
            print("Reactive Power Profile Data:")
            print(self.reactive_power_profile)
        else:
            print("No Reactive power profile data provided.")
