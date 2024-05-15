import json
import pprint
import warnings
from pandas import DataFrame
from power_grid_model import PowerGridModel
from power_grid_model.utils import json_deserialize, json_serialize

class PowerFlow:
    """
    General documentation of this class.
    You need to describe the purpose of this class and the functions in it.
    We are using an undirected graph in the processor.
    """
    def __init__(self):
        # Load data upon instantiation
        self.load_data()

    def load_data(self):
        # Open the file and read its content
        with open("src/power_system_simulation/input_network_data.json") as fp:
            # Assign the file content to the data attribute
            self.data = fp.read()

    def process_data(self):
        pprint.pprint(json.loads(self.data))
        dataset = json_deserialize(self.data)
        print("components:", dataset.keys())
        print(DataFrame(dataset["node"]))

        model = PowerGridModel(dataset)
        output = model.calculate_power_flow()
        print(DataFrame(output["node"]))

        serialized_output = json_serialize(output)
        print(serialized_output)

# Instantiate the class
power_flow_instance = PowerFlow()

# Call the method to process the data
power_flow_instance.process_data()
