# test_main.py

import unittest
from power_system_simulation.EV_penetration_lvl import process_evs

class TestProcessEVs(unittest.TestCase):

    def test_process_evs(self):
        # Define input data
        number_of_houses = 150
        number_of_feeders = 7
        penetration_level = 0.20

        # Call the function with the input data
        evs_per_feeder = process_evs(
            number_of_houses, number_of_feeders, penetration_level
        )

        # Check that the evs_per_feeder is an integer
        self.assertIsInstance(evs_per_feeder, int)



if __name__ == "__main__":
    unittest.main()