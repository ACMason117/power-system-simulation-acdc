import unittest

import pandas as pd
import pytest
from power_grid_model.utils import json_deserialize_from_file


class TestPowerFlow(unittest.TestCase):

    def test_process_data(self):
        # Import the PowerFlow class here to avoid circular import
        from power_system_simulation.power_flow_processing import PowerFlow

        # Load data from input_network_data.json
        test_data = json_deserialize_from_file("src/power_system_simulation/input_network_data.json")

        # Load the Active Power Profile file
        try:
            power_profile = pd.read_parquet("src/power_system_simulation/active_power_profile.parquet")
        except FileNotFoundError:
            self.fail(
                "Active Power Profile file not found. Please ensure 'src/power_system_simulation/active_power_profile.parquet' is in the correct location."
            )
            return

        # Load the Reactive Power Profile file
        try:
            reactive_power_profile = pd.read_parquet("src/power_system_simulation/reactive_power_profile.parquet")
        except FileNotFoundError:
            self.fail(
                "Reactive Power Profile file not found. Please ensure 'src/power_system_simulation/reactive_power_profile.parquet' is in the correct location."
            )
            return

        # Instantiate the PowerFlow class with test data and power profiles
        power_flow_instance = PowerFlow(grid_data=test_data)

        # # Call the method to process the data
        # print("Running process_data and printing profile data:")
        # power_flow_instance.process_data()


if __name__ == "__main__":
    unittest.main()
