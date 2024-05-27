# power_flow_processing.py
"""
In this file the processing of the power system should be done. Power system can be given in a different test file. 
"""

import json
import pprint
import pandas as pd

from pandas import DataFrame
from power_grid_model import PowerGridModel
from power_grid_model.utils import json_deserialize, json_serialize

import time
from typing import Dict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from power_grid_model import (
    PowerGridModel,
    CalculationType,
    CalculationMethod,
    initialize_array
)

from power_grid_model.validation import (
    assert_valid_input_data,
    assert_valid_batch_data
)

class PowerFlow:
    """
    General documentation of this class.
    You need to describe the purpose of this class and the functions in it.
    We are initializing the data here.
    """

    def __init__(self, data=None, power_profile=None, reactive_power_profile=None):
        # Load data upon instantiation
        self.data = data
        self.power_profile = power_profile
        self.reactive_power_profile = reactive_power_profile

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

        if self.power_profile is not None:
            print("Active Power Profile Data:")
            print(self.power_profile)
        else:
            print("No active power profile data provided.")

        if self.reactive_power_profile is not None:
            print("Reactive Power Profile Data:")
            print(self.reactive_power_profile)
        else:
            print("No Reactive power profile data provided.")

    def aggregate_power_flow_result_table1(data):
        result = []
        model = PowerGridModel(input_data=data)
        result1 = model.calculate_power_flow(calculation_method=CalculationMethod.linear)
        max_voltage = max(result1["node"]["u_pu"])
        min_voltage = min(result1["node"]["u_pu"])

        for i in range(len(result1["node"]["u_pu"])):
            if result1["node"]["u_pu"][i] == max_voltage:
                max_node = result1["node"]["id"][i]
            if result1["node"]["u_pu"][i] == min_voltage:
                min_node = result1["node"]["id"][i]

        result.append({
                'Timestamp':["Node"], # I am not sure about this
                'Max p.u. voltage': max_voltage,
                'Max voltage node id': max_node,
                'Min p.u. voltage': min_voltage,
                'Min Voltage node id': min_node
        })

        # Convert the list of dictionaries to a Pandas Dataframe
        result_df = pd.DataFrame(result)
        # Set the timestamp column as the index
        result_df.set_index('Timestamp', inplace=True)
        return result_df