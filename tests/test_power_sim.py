import unittest
from datetime import datetime

import numpy as np
import pandas as pd
import scipy as sp
from power_grid_model.utils import json_deserialize_from_file

import power_system_simulation.graph_processing as gp
import power_system_simulation.power_flow_processing as pfp
import power_system_simulation.power_system_simulation as pss


class TestPowerSim(unittest.TestCase):
    def setUp(self):
        # Load data from input_network_data.json
        self.grid_data = json_deserialize_from_file("src/power_system_simulation/input_network_data_2.json")

        # Load the Active Power Profile file
        try:
            self.active_power_profile = pd.read_parquet(
                "src/power_system_simulation/active_power_profile_2.parquet"
            )
        except FileNotFoundError:
            self.fail(
                "Active Power Profile file not found. Please ensure 'active_power_profile.parquet' is in the correct location."
            )

        # Load the EV active power profile file
        try:
            self.ev_active_power_profile = pd.read_parquet(
                "src/power_system_simulation/ev_active_power_profile_2.parquet"
            )
        except FileNotFoundError:
            self.fail(
                "EV Active Power Profile file not found. Please ensure 'active_power_profile.parquet' is in the correct location."
            )

        # Load the Reactive Power Profile file
        try:
            self.reactive_power_profile = pd.read_parquet(
                "src/power_system_simulation/reactive_power_profile_2.parquet"
            )
        except FileNotFoundError:
            self.fail(
                "Reactive Power Profile file not found. Please ensure 'reactive_power_profile.parquet' is in the correct location."
            )

        # declare new PowerSimModel object
        self.psm = pss.PowerSim(grid_data=self.grid_data)

    def test_N1(self):
        disabled_edge_id = 16
        table = self.psm.n1_calculations(
            self.grid_data, self.active_power_profile, self.reactive_power_profile, disabled_edge_id
        )

        self.assertIsInstance(table, pd.DataFrame)
        self.assertListEqual(
            list(table.columns),
            ["Alternative_Line_ID", "Max_Loading", "Max_Loading_ID", "Max_Loading_Timestamp"],
        )

        expected_output = pd.DataFrame(
            {
                "Alternative_Line_ID": [24],
                "Max_Loading": [0.0016589657345386518],
                "Max_Loading_ID": [21],
                "Max_Loading_Timestamp": [pd.Timestamp("2025-01-07 10:30:00")],
            }
        )

        expected_output["Alternative_Line_ID"] = expected_output["Alternative_Line_ID"].astype(np.int32)
        expected_output["Max_Loading_ID"] = expected_output["Max_Loading_ID"].astype(np.int32)

        # Compare with expected output
        pd.testing.assert_frame_equal(table, expected_output)

    def test_EV_penetration(self):
        num_houses = 150
        penetration_level = 20
        num_feeders = 7

        voltage_table, loading_table = self.psm.ev_penetration(
            num_houses=num_houses,
            num_feeders=num_feeders,
            penetration_level=penetration_level,
            active_power_profile=self.active_power_profile,
            reactive_power_profile=self.reactive_power_profile,
            ev_active_power_profile=self.ev_active_power_profile
        )

        # Assertions to verify correct functionality
        # Ensure voltage_table and loading_table are DataFrames
        self.assertIsInstance(voltage_table, pd.DataFrame)
        self.assertIsInstance(loading_table, pd.DataFrame)

        # Check if voltage_table and loading_table have the expected structure
        self.assertFalse(voltage_table.empty, "Voltage table should not be empty")
        self.assertFalse(loading_table.empty, "Loading table should not be empty")



if __name__ == "__main__":
    unittest.main()
