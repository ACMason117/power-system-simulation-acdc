import unittest
import pandas as pd
from power_system_simulation.power_flow_processing import PowerFlow

class TestPowerFlow(unittest.TestCase):

    def test_process_data(self):
        # Load data from input_network_data.json
        with open("src/power_system_simulation/input_network_data.json") as file:
            test_data = file.read()

        # Load the Parquet file
        try:
            power_profile = pd.read_parquet("src/power_system_simulation/active_power_profile.parquet")
        except FileNotFoundError:
            self.fail("Parquet file not found. Please ensure 'src/power_system_simulation/active_power_profile.parquet' is in the correct location.")
            return

        # Instantiate the PowerFlow class with test data and power profile
        power_flow_instance = PowerFlow(data=test_data, power_profile=power_profile)

        # Call the method to process the data
        print("Running process_data and printing active power profile data:")
        power_flow_instance.process_data()

if __name__ == "__main__":
    unittest.main()
