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
        self.grid_data = json_deserialize_from_file("src/power_system_simulation/input_network_data_assign3.json")

        # Load the Active Power Profile file
        try:
            self.active_power_profile = pd.read_parquet(
                "src/power_system_simulation/active_power_profile_assign3.parquet"
            )
        except FileNotFoundError:
            self.fail(
                "Active Power Profile file not found. Please ensure 'active_power_profile.parquet' is in the correct location."
            )

        # Load the Reactive Power Profile file
        try:
            self.reactive_power_profile = pd.read_parquet(
                "src/power_system_simulation/reactive_power_profile_assign3.parquet"
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


if __name__ == "__main__":
    unittest.main()
