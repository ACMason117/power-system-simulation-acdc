import unittest
from datetime import datetime

import pandas as pd
import scipy as sp
from power_grid_model.utils import json_deserialize_from_file

import power_system_simulation.power_flow_processing as pfp


class TestPowerFlow(unittest.TestCase):

    def setUp(self):
        # Load data from input_network_data.json
        self.grid_data = json_deserialize_from_file("src/power_system_simulation/input_network_data.json")

        # Load the Active Power Profile file
        try:
            self.active_power_profile = pd.read_parquet("src/power_system_simulation/active_power_profile.parquet")
        except FileNotFoundError:
            self.fail(
                "Active Power Profile file not found. Please ensure 'active_power_profile.parquet' is in the correct location."
            )

        # Load the Reactive Power Profile file
        try:
            self.reactive_power_profile = pd.read_parquet("src/power_system_simulation/reactive_power_profile.parquet")
        except FileNotFoundError:
            self.fail(
                "Reactive Power Profile file not found. Please ensure 'reactive_power_profile.parquet' is in the correct location."
            )

        # Load the expected output data for comparison
        try:
            self.expected_output_table_row_per_line = pd.read_parquet(
                "src/power_system_simulation/output_table_row_per_line.parquet"
            )
            self.expected_output_table_row_per_timestamp = pd.read_parquet(
                "src/power_system_simulation/output_table_row_per_timestamp.parquet"
            )
        except FileNotFoundError:
            self.fail(
                "Expected output files not found. Please ensure 'output_table_row_per_line.parquet' and 'output_table_row_per_timestamp.parquet' are in the correct location."
            )

        # Instantiate the PowerFlow class with test data and power profiles
        self.pf = pfp.PowerFlow(grid_data=self.grid_data)

    def test_batch_powerflow(self):
        output_data = self.pf.batch_powerflow(self.active_power_profile, self.reactive_power_profile)
        self.assertIsInstance(output_data, dict)

        # Optionally, if there are specific expected outputs for the batch power flow,
        # those can be compared here as well. For now, we assume output_data validation
        # is done through the other methods.

    def test_aggregate_voltage_table(self):
        voltage_table = self.pf.aggregate_voltage_table(self.active_power_profile, self.reactive_power_profile)
        self.assertIsInstance(voltage_table, pd.DataFrame)
        self.assertListEqual(
            list(voltage_table.columns), ["Max_Voltage", "Max_Voltage_Node", "Min_Voltage", "Min_Voltage_Node"]
        )

        # Compare with expected output
        pd.testing.assert_frame_equal(voltage_table, self.expected_output_table_row_per_timestamp)

    def test_aggregate_loading_table(self):
        loading_table = self.pf.aggregate_loading_table(self.active_power_profile, self.reactive_power_profile)
        self.assertIsInstance(loading_table, pd.DataFrame)
        self.assertListEqual(
            list(loading_table.columns),
            ["Total_Loss", "Max_Loading", "Max_Loading_Timestamp", "Min_Loading", "Min_Loading_Timestamp"],
        )

        # Compare with expected output
        pd.testing.assert_frame_equal(loading_table, self.expected_output_table_row_per_line)

    def test_no_active_power_profile(self):
        with self.assertRaises(pfp.PowerProfileNotFound):
            self.pf.batch_powerflow(None, self.reactive_power_profile)

    def test_no_reactive_power_profile(self):
        with self.assertRaises(pfp.PowerProfileNotFound):
            self.pf.batch_powerflow(self.active_power_profile, None)

    def test_timestamp_mismatch(self):
        reactive_power_profile = self.reactive_power_profile.copy()
        # Ensure the reactive power profile has a different number of timestamps
        reactive_power_profile.index = pd.date_range(
            start="2024-06-01", periods=len(self.reactive_power_profile), freq="H"
        )
        with self.assertRaises(pfp.TimestampMismatch):
            self.pf.batch_powerflow(self.active_power_profile, reactive_power_profile)

    def test_load_id_mismatch(self):
        reactive_power_profile = self.reactive_power_profile.copy()
        # Ensure the reactive power profile has different load IDs but same number of columns
        columns = reactive_power_profile.columns.tolist()
        columns[0] = "new_load_id"
        reactive_power_profile.columns = columns
        with self.assertRaises(pfp.LoadIDMismatch):
            self.pf.batch_powerflow(self.active_power_profile, reactive_power_profile)


if __name__ == "__main__":
    unittest.main()
