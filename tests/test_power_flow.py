import unittest
from power_system_simulation.power_flow_processing import PowerFlow

class TestPowerFlow(unittest.TestCase):

    def test_process_data(self):
        # Load data from input_network_data.json
        with open("src/power_system_simulation/input_network_data.json") as file:
            test_data = file.read()

        # Instantiate the PowerFlow class with test data
        power_flow_instance = PowerFlow(data=test_data)

        # Call the method to process the data
        power_flow_instance.process_data()


if __name__ == "__main__":
    unittest.main()
