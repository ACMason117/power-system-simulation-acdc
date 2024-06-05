import unittest

import pandas as pd
import pytest
from power_grid_model.utils import json_deserialize_from_file

import power_system_simulation.optimal_tap_position as otp

# Import the PowerFlow class here to avoid circular import
from power_system_simulation.optimal_tap_position import OptimalTapPosition


class TestOptimalTapPosition(unittest.TestCase):

    def setUp(self):

        # Load data from input_network_data1.json
        self.grid_data = json_deserialize_from_file("src/power_system_simulation/input_network_data1.json")

        # Load the Active Power Profile file
        try:
            self.active_power_profile1 = pd.read_parquet("src/power_system_simulation/active_power_profile1.parquet")
        except FileNotFoundError:
            self.fail(
                "Active Power Profile file not found. Please ensure 'src/power_system_simulation/active_power_profile1.parquet' is in the correct location."
            )
            return

        # Load the Reactive Power Profile file
        try:
            self.reactive_power_profile1 = pd.read_parquet(
                "src/power_system_simulation/reactive_power_profile1.parquet"
            )
        except FileNotFoundError:
            self.fail(
                "Reactive Power Profile file not found. Please ensure 'src/power_system_simulation/reactive_power_profile1.parquet' is in the correct location."
            )
            return

        # Instantiate the optimal_tap_position_instance class with test data and power profiles
        optimal_tap_position_instance = OptimalTapPosition(grid_data=self.grid_data)

        self.pf = otp.PowerFlow(grid_data=self.grid_data)

    def optimal_tap_voltage(self):
        tap_value_voltage = self.otp.optimal_tap_voltage(self.active_power_profile1, self.reactive_power_profile1)
        self.assertIsInstance(tap_value_voltage, dict)


if __name__ == "__main__":
    unittest.main()
