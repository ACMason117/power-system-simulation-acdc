# power_flow_processing.py
"""
In this file the processing of the power system should be done. Power system can be given in a different test file. 
"""

import json
import pprint

from pandas import DataFrame
from power_grid_model import PowerGridModel
from power_grid_model.utils import json_deserialize, json_serialize


class PowerFlow:
    """
    General documentation of this class.
    You need to describe the purpose of this class and the functions in it.
    We are initializing the data here.
    """

    def __init__(self, data=None):
        # Load data upon instantiation
        if data is not None:
            self.data = data
        else:
            self.load_data()

    def load_data(self):
        """
        Open the file and read its content
        """
        with open("src/power_system_simulation/input_network_data.json") as fp:
            # Assign the file content to the data attribute
            self.data = fp.read()

    def process_data(self):
        """
        Do the processing of the data here.
        """
        pprint.pprint(json.loads(self.data))
        dataset = json_deserialize(self.data)
        print("components:", dataset.keys())
        print(DataFrame(dataset["node"]))

        model = PowerGridModel(dataset)
        output = model.calculate_power_flow()
        print(DataFrame(output["node"]))

        serialized_output = json_serialize(output)
        print(serialized_output)
