# power_flow_processing.py
"""
In this file the processing of the power system should be done. Power system can be given in a different test file. 
"""

import json
import pprint
import warnings

# import pyarrow.parquet as pq
# import pyarrow as pa
# import power_grid_model as pgm

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

        # Construct PGM
        self.model = PowerGridModel(self.grid_data)

        self.output_data = self.model.calculate_state_estimation(symmetric=True)

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

        serialized_output = json_serialize(output)
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
