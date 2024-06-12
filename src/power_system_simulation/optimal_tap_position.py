# optimal_tap_position.py
"""
In this file the optimal tap position 
"""

import json
import pprint
import warnings

import numpy as np
import pandas as pd

# import power_grid_model as pgm
import pyarrow as pa
import pyarrow.parquet as pq
import scipy as sp

with warnings.catch_warnings(action="ignore", category=DeprecationWarning):
    # suppress warning about pyarrow as future required dependency
    from pandas import DataFrame

from power_grid_model import (
    BranchSide,
    CalculationMethod,
    CalculationType,
    LoadGenType,
    MeasuredTerminalType,
    PowerGridModel,
    TapChangingStrategy,
    initialize_array,
)
from power_grid_model.utils import json_deserialize, json_serialize
from power_grid_model.validation import assert_valid_batch_data, assert_valid_input_data
from pyarrow import table

from power_system_simulation.power_flow_processing import pfp


class PowerProfileNotFound(Exception):
    """Raises error if power profile is not found"""

    pass


class TimestampMismatch(Exception):
    """ " Raises error if timestamps of power profiles do no not match"""

    pass


class LoadIDMismatch(Exception):
    """ " Raises error if load IDs of power profiles do no not match"""

    pass


class OptimalTapPosition:

    def __init__(self, grid_data: dict) -> None:
        """Load grid_data in class 'PowerFlow' upon instantiation

        Args:
            grid_data: Power grid input data. Class dict.
            active_power_profile: Active power profile time data. Class pyarrow.table.
            reactive_power_profile: Reactive power profile time data. Class pyarrow.table.
        """

        assert_valid_input_data(input_data=grid_data, symmetric=True, calculation_type=CalculationType.power_flow)

        self.grid_data = grid_data

        self.model = PowerGridModel(self.grid_data)

        self.Power_flow_instance = pfp.PowerFlow(self.grid_data)

    def tap_position(self, active_power_profile1: pd.DataFrame, reactive_power_profile1: pd.DataFrame) -> pd.DataFrame:

        output_data = pfp.Power_flow_instance.batch_powerflow(
            active_power_profile=active_power_profile1, reactive_power_profile=reactive_power_profile1
        )

        tap_position = 0
        for i in range(len(output_data["node"]["id"])):
            if isinstance(output_data["node"]["id"][i], (list, np.ndarray)):
                for j in range(len(output_data["node"]["id"][i])):
                    if output_data["node"]["id"][i][j] == self.grid_data["transformer"]["from_node"]:
                        tap = (
                            (output_data["node"]["u"][i][j] - self.grid_data["transformer"]["u1"])
                            / (self.grid_data["transformer"]["u1"])
                        ) * 100
                        tap_position = tap + tap_position

        optimial_tap_position = tap_position / (len(output_data["node"]["id"]))

        return optimial_tap_position

    def optimal_tap_voltage(
        self, active_power_profile1: pd.DataFrame, reactive_power_profile1: pd.DataFrame
    ) -> pd.DataFrame:

        tap_voltage = 0

        voltage_table = PowerFlow.aggregate_voltage_table(
            active_power_profile=active_power_profile1, reactive_power_profile=reactive_power_profile1
        )

        for i in range(len(voltage_table)):
            u_pu_max = voltage_table["Max_Voltage"].iloc[i]
            u_pu_min = voltage_table["Min_Voltage"].iloc[i]
            tap_max = ((u_pu_max - 1) / 1) * 100
            tap_min = ((u_pu_min - 1) / 1) * 100
            tap_voltage = tap_max + tap_min + tap_voltage

        tap_position_voltage = tap_voltage / (2 * (len(voltage_table)))

        return tap_position_voltage