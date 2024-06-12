import unittest
import pandas as pd
from power_system_simulation.power_flow_processing import PowerFlow
from power_system_simulation.power_system_simulation import PowerSim

class TestProcessEVs(unittest.TestCase):
    
    def setUp(self):
        self.grid_data = {
            # Sample grid data
        }
        self.sim = PowerSim(self.grid_data)

    def test_ev_penetration(self):
        # Define input data
        number_of_houses = 150
        number_of_feeders = 7
        penetration_level = 0.20

        # Call the method with the input data
        evs_per_feeder = self.sim.ev_penetration(
            number_of_houses, number_of_feeders, penetration_level
        )

        # Check that the evs_per_feeder is an integer
        self.assertIsInstance(evs_per_feeder, int)

if __name__ == "__main__":
    unittest.main()
