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
import numpy as np

with warnings.catch_warnings(action="ignore", category=DeprecationWarning):
    # suppress warning about pyarrow as future required dependency
    from pandas import DataFrame

from power_grid_model import CalculationMethod, CalculationType, PowerGridModel, initialize_array
from power_grid_model.utils import json_deserialize, json_serialize
from power_grid_model.validation import assert_valid_batch_data, assert_valid_input_data
from pyarrow import table

from power_system_simulation.power_flow_processing import PowerFlow

from power_grid_model import LoadGenType
from power_grid_model import (
    PowerGridModel,
    CalculationMethod,
    CalculationType,
    MeasuredTerminalType,
    BranchSide,
    TapChangingStrategy,
)
from power_grid_model import initialize_array


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

    def tap_position(self, active_power_profile1: pd.DataFrame, reactive_power_profile1: pd.DataFrame) -> pd.DataFrame:

        output_data = PowerFlow.batch_powerflow(
            active_power_profile=active_power_profile1, reactive_power_profile=reactive_power_profile1
        )

        a = {}
        tap_pro = {}
        for i in range(len(output_data["node"]["id"])):
            if isinstance(output_data["node"]["id"][i], (list, np.ndarray)):
                for j in range(len(output_data["node"]["id"][i])):
                    if output_data["node"]["id"][i][j] == 0:
                        a[i] = output_data["node"]["u"][i][j]
            elif output_data["node"]["id"][i] == 0:
                a[i] = output_data["node"]["u"][i]
        
        tap_position = 0
        for i in range(len(a)):
            tap_pro[i] = ((a[i] - self.grid_data["transformer"]["u1"]) / self.grid_data["transformer"]["u1"]) * 100
            tap_position = tap_pro + tap_position

        Optimal_tap_position = tap_position/(len(output_data["node"]["id"]))

        return Optimal_tap_position

    def optimal_tap_voltage(
        self, active_power_profile1: pd.DataFrame, reactive_power_profile1: pd.DataFrame
    ) -> pd.DataFrame:
        tap = 0

        voltage_table = PowerFlow.aggregate_voltage_table(
            active_power_profile=active_power_profile1, reactive_power_profile=reactive_power_profile1
        )

        for i in range(len(voltage_table)):
            u_pu_max = voltage_table["Max_Voltage"][i]
            u_pu_min = voltage_table["Min_Voltage"][i]
            tap_procent_max = (u_pu_max - 1) / 1 * 100
            tap_procent_min = (u_pu_min - 1) / 1 * 100
            tap_max_min = (tap_procent_max + tap_procent_min) / 2
            tap = tap_max_min + tap

        tap_value_voltage = tap / (len(voltage_table))

        return tap_value_voltage
   