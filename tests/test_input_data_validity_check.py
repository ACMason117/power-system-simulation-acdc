import unittest

from power_grid_model import LoadGenType
from power_grid_model import PowerGridModel
from power_grid_model import initialize_array

import pandas as pd
import pytest  # Import pytest

from power_system_simulation.input_data_validity_check import InvalidLVFeederIDError, validity_check  # Import power_system_simpulation.graphy_processing
from power_system_simulation.power_flow_processing import PowerFlow

def test_validity():

    # node
    node = initialize_array('input', 'node', 2)
    node['id'] = [1, 2]
    node['u_rated'] = [10.5e3, 10.5e3]
    # line
    line = initialize_array('input', 'line', 1)
    line['id'] = [3]
    line['from_node'] = [1]
    line['to_node'] = [2]
    line['from_status'] = [1]
    line['to_status'] = [1]
    line['r1'] = [0.25]
    line['x1'] = [0.2]
    line['c1'] = [10e-6]
    line['tan1'] = [0.0]
    line['i_n'] = [1000]
    # load
    sym_load = initialize_array('input', 'sym_load', 1)
    sym_load['id'] = [4]
    sym_load['node'] = [2]
    sym_load['status'] = [1]
    sym_load['type'] = [LoadGenType.const_power]
    sym_load['p_specified'] = [2e6]
    sym_load['q_specified'] = [0.5e6]
    # source
    source = initialize_array('input', 'source', 1)
    source['id'] = [5]
    source['node'] = [1]
    source['status'] = [1]
    source['u_ref'] = [1.0]
    # all
    input_data = {
        'node': node,
        'line': line,
        'sym_load': sym_load,
        'source': source
    }

    lv_feeders=[2,3]

    with pytest.raises(InvalidLVFeederIDError) as excinfo:
       validity_check(grid_data=input_data, lv_feeders=lv_feeders)
    assert str(excinfo.value) == "Vertex IDs are not unique"

# class TestValidityCheck(unittest.TestCase):

#     def test(self):

#         # Load data from input_network_data_2.json
#         with open("src/power_system_simulation/input_network_data_2.json") as file:
#             test_data = file.read()

#         # Load data from meta_data.json
#         with open("src/power_system_simulation/meta_data_2.json") as file:
#             meta_data = file.read()

#         # Load the Active Power Profile file
#         try:
#             active_power_profile = pd.read_parquet("src/power_system_simulation/active_power_profile_2.parquet")
#         except FileNotFoundError:
#             self.fail(
#                 "Active Power Profile file not found. Please ensure 'src/power_system_simulation/active_power_profile_2.parquet' is in the correct location."
#             )
#             return

#         # Load the Reactive Power Profile file
#         try:
#             reactive_power_profile = pd.read_parquet("src/power_system_simulation/reactive_power_profile_2.parquet")
#         except FileNotFoundError:
#             self.fail(
#                 "Reactive Power Profile file not found. Please ensure 'src/power_system_simulation/reactive_power_profile_2.parquet' is in the correct location."
#             )
#             return
        
#          # Instantiate the PowerFlow class with test data and power profiles
#         power_flow_instance = PowerFlow(
#             grid_data=test_data, active_power_profile=active_power_profile, reactive_power_profile=reactive_power_profile
#         )

#         # Call the method to process the data
#         print("Running process_data and printing profile data:")
#         power_flow_instance.process_data()

        #with pytest.raises(InvalidLVFeederIDError) as excinfo:
        #    validity_check(grid_data=test_data, lv_feeders=meta_data[4], active_power_profile=active_power_profile, reactive_power_profile=reactive_power_profile)
        #assert str(excinfo.value) == "Vertex IDs are not unique"
        
        

        


# if __name__ == "__main__":
#     unittest.main()

    