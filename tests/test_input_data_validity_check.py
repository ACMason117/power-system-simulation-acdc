import unittest
from datetime import datetime

import scipy as sp
from power_grid_model.utils import json_deserialize_from_file

import power_system_simulation.power_flow_processing as pfp
import power_system_simulation.power_system_simulation as pss


import pandas as pd
import pytest  # Import pytest
from power_grid_model import LoadGenType, PowerGridModel, initialize_array

from power_system_simulation.graph_processing import GraphCycleError, GraphNotFullyConnectedError

# from power_system_simulation.input_data_validity_check import InvalidLVFeederIDError, validity_check, NotExactlyOneSourceError, NotExactlyOneTransformerError, WrongFromNodeLVFeederError  # Import power_system_simpulation.graphy_processing
from power_system_simulation.power_flow_processing import PowerFlow
from power_system_simulation.power_system_simulation import (
    InvalidLVFeederIDError,
    NotExactlyOneSourceError,
    NotExactlyOneTransformerError,
    PowerSim,
    WrongFromNodeLVFeederError,
)


def test_InvalidLVFeederIDError():

    # node
    node = initialize_array("input", "node", 3)
    node["id"] = [2, 4, 6]
    node["u_rated"] = [1e4, 4e2, 4e2]

    # load
    sym_load = initialize_array("input", "sym_load", 1)
    sym_load["id"] = [7]
    sym_load["node"] = [6]
    sym_load["status"] = [1]
    sym_load["type"] = [LoadGenType.const_power]
    sym_load["p_specified"] = [1e3]
    sym_load["q_specified"] = [5e3]

    # source
    source = initialize_array("input", "source", 1)
    source["id"] = [1]
    source["node"] = [2]
    source["status"] = [1]
    source["u_ref"] = [1.0]

    # line
    line = initialize_array("input", "line", 1)
    line["id"] = [5]
    line["from_node"] = [4]
    line["to_node"] = [6]
    line["from_status"] = [1]
    line["to_status"] = [1]
    line["r1"] = [10.0]
    line["x1"] = [0.0]
    line["c1"] = [0.0]
    line["tan1"] = [0.0]

    # transformer
    transformer = initialize_array("input", "transformer", 1)
    transformer["id"] = [3]
    transformer["from_node"] = [2]
    transformer["to_node"] = [4]
    transformer["from_status"] = [1]
    transformer["to_status"] = [1]
    transformer["u1"] = [1e4]
    transformer["u2"] = [4e2]
    transformer["sn"] = [1e5]
    transformer["uk"] = [0.1]
    transformer["pk"] = [1e3]
    transformer["i0"] = [1.0e-6]
    transformer["p0"] = [0.1]
    transformer["winding_from"] = [2]
    transformer["winding_to"] = [1]
    transformer["clock"] = [5]
    transformer["tap_side"] = [0]
    transformer["tap_pos"] = [3]
    transformer["tap_min"] = [-11]
    transformer["tap_max"] = [9]
    transformer["tap_size"] = [100]

    # all
    input_data = {"node": node, "line": line, "sym_load": sym_load, "source": source, "transformer": transformer}

    with pytest.raises(InvalidLVFeederIDError) as excinfo:
        lv_feeders = [2]
        PowerSim(grid_data=input_data, lv_feeders=lv_feeders)
    assert str(excinfo.value) == "LV feeder IDs are not valid line IDs"

    with pytest.raises(InvalidLVFeederIDError) as excinfo:
        lv_feeders = [20]
        PowerSim(grid_data=input_data, lv_feeders=lv_feeders)
    assert str(excinfo.value) == "LV feeder IDs are not valid line IDs"


def test_NotExactlyOneSourceError():

    # node
    node = initialize_array("input", "node", 3)
    node["id"] = [2, 4, 6]
    node["u_rated"] = [1e4, 4e2, 4e2]

    # load
    sym_load = initialize_array("input", "sym_load", 1)
    sym_load["id"] = [7]
    sym_load["node"] = [6]
    sym_load["status"] = [1]
    sym_load["type"] = [LoadGenType.const_power]
    sym_load["p_specified"] = [1e3]
    sym_load["q_specified"] = [5e3]

    # line
    line = initialize_array("input", "line", 1)
    line["id"] = [5]
    line["from_node"] = [4]
    line["to_node"] = [6]
    line["from_status"] = [1]
    line["to_status"] = [1]
    line["r1"] = [10.0]
    line["x1"] = [0.0]
    line["c1"] = [0.0]
    line["tan1"] = [0.0]

    # transformer
    transformer = initialize_array("input", "transformer", 1)
    transformer["id"] = [3]
    transformer["from_node"] = [2]
    transformer["to_node"] = [4]
    transformer["from_status"] = [1]
    transformer["to_status"] = [1]
    transformer["u1"] = [1e4]
    transformer["u2"] = [4e2]
    transformer["sn"] = [1e5]
    transformer["uk"] = [0.1]
    transformer["pk"] = [1e3]
    transformer["i0"] = [1.0e-6]
    transformer["p0"] = [0.1]
    transformer["winding_from"] = [2]
    transformer["winding_to"] = [1]
    transformer["clock"] = [5]
    transformer["tap_side"] = [0]
    transformer["tap_pos"] = [3]
    transformer["tap_min"] = [-11]
    transformer["tap_max"] = [9]
    transformer["tap_size"] = [100]

    lv_feeders = []

    with pytest.raises(NotExactlyOneSourceError) as excinfo:
        # source
        source = initialize_array("input", "source", 2)
        source["id"] = [1, 10]
        source["node"] = [2, 4]
        source["status"] = [1, 1]
        source["u_ref"] = [1.0, 1.0]
        # all
        input_data = {"node": node, "line": line, "sym_load": sym_load, "source": source, "transformer": transformer}
        PowerSim(grid_data=input_data, lv_feeders=lv_feeders)
    assert str(excinfo.value) == "There is not exactly one source"

    with pytest.raises(NotExactlyOneSourceError) as excinfo:
        # source
        source = initialize_array("input", "source", 0)
        source["id"] = []
        source["node"] = []
        source["status"] = []
        source["u_ref"] = []
        # all
        input_data = {"node": node, "line": line, "sym_load": sym_load, "source": source, "transformer": transformer}
        PowerSim(grid_data=input_data, lv_feeders=lv_feeders)
    assert str(excinfo.value) == "There is not exactly one source"


def test_NotExactlyOneTransformerError():

    # node
    node = initialize_array("input", "node", 3)
    node["id"] = [2, 4, 6]
    node["u_rated"] = [1e4, 4e2, 4e2]

    # load
    sym_load = initialize_array("input", "sym_load", 1)
    sym_load["id"] = [7]
    sym_load["node"] = [6]
    sym_load["status"] = [1]
    sym_load["type"] = [LoadGenType.const_power]
    sym_load["p_specified"] = [1e3]
    sym_load["q_specified"] = [5e3]

    # line
    line = initialize_array("input", "line", 1)
    line["id"] = [5]
    line["from_node"] = [4]
    line["to_node"] = [6]
    line["from_status"] = [1]
    line["to_status"] = [1]
    line["r1"] = [10.0]
    line["x1"] = [0.0]
    line["c1"] = [0.0]
    line["tan1"] = [0.0]

    # source
    source = initialize_array("input", "source", 1)
    source["id"] = [1]
    source["node"] = [2]
    source["status"] = [1]
    source["u_ref"] = [1.0]

    lv_feeders = [5]

    with pytest.raises(NotExactlyOneTransformerError) as excinfo:
        # node
        node = initialize_array("input", "node", 4)
        node["id"] = [2, 4, 6, 8]
        node["u_rated"] = [1e4, 4e2, 4e2, 4e2]
        # transformer
        transformer = initialize_array("input", "transformer", 2)
        transformer["id"] = [3, 10]
        transformer["from_node"] = [2, 6]
        transformer["to_node"] = [4, 8]
        transformer["from_status"] = [1, 1]
        transformer["to_status"] = [1, 1]
        transformer["u1"] = [1e4, 4e2]
        transformer["u2"] = [4e2, 4e2]
        transformer["sn"] = [1e5, 1e5]
        transformer["uk"] = [0.1, 0.1]
        transformer["pk"] = [1e3, 1e3]
        transformer["i0"] = [1.0e-6, 1.0e-6]
        transformer["p0"] = [0.1, 0.1]
        transformer["winding_from"] = [2, 2]
        transformer["winding_to"] = [1, 2]
        transformer["clock"] = [5, 6]
        transformer["tap_side"] = [0, 0]
        transformer["tap_pos"] = [3, 3]
        transformer["tap_min"] = [-11, -11]
        transformer["tap_max"] = [9, 9]
        transformer["tap_size"] = [100, 100]
        # all
        input_data = {"node": node, "line": line, "sym_load": sym_load, "source": source, "transformer": transformer}
        PowerSim(grid_data=input_data, lv_feeders=lv_feeders)
    assert str(excinfo.value) == "There is not exactly one transformer"

    with pytest.raises(NotExactlyOneTransformerError) as excinfo:
        # transformer
        transformer = initialize_array("input", "transformer", 0)
        transformer["id"] = []
        transformer["from_node"] = []
        transformer["to_node"] = []
        transformer["from_status"] = []
        transformer["to_status"] = []
        transformer["u1"] = []
        transformer["u2"] = []
        transformer["sn"] = []
        transformer["uk"] = []
        transformer["pk"] = []
        transformer["i0"] = []
        transformer["p0"] = []
        transformer["winding_from"] = []
        transformer["winding_to"] = []
        transformer["clock"] = []
        transformer["tap_side"] = []
        transformer["tap_pos"] = []
        transformer["tap_min"] = []
        transformer["tap_max"] = []
        transformer["tap_size"] = []
        # all
        input_data = {"node": node, "line": line, "sym_load": sym_load, "source": source, "transformer": transformer}
        PowerSim(grid_data=input_data, lv_feeders=lv_feeders)
    assert str(excinfo.value) == "There is not exactly one transformer"


def test_WrongFromNodeLVFeederError():

    # node
    node = initialize_array("input", "node", 4)
    node["id"] = [2, 4, 6, 8]
    node["u_rated"] = [1e4, 4e2, 4e2, 4e2]

    # source
    source = initialize_array("input", "source", 1)
    source["id"] = [1]
    source["node"] = [2]
    source["status"] = [1]
    source["u_ref"] = [1.0]

    # load
    sym_load = initialize_array("input", "sym_load", 1)
    sym_load["id"] = [7]
    sym_load["node"] = [6]
    sym_load["status"] = [1]
    sym_load["type"] = [LoadGenType.const_power]
    sym_load["p_specified"] = [1e3]
    sym_load["q_specified"] = [5e3]

    # line
    line = initialize_array("input", "line", 2)
    line["id"] = [5, 10]
    line["from_status"] = [1, 1]
    line["to_status"] = [1, 1]
    line["r1"] = [10.0, 10.00]
    line["x1"] = [0.0, 0.0]
    line["c1"] = [0.0, 0.0]
    line["tan1"] = [0.0, 0.0]

    # transformer
    transformer = initialize_array("input", "transformer", 1)
    transformer["id"] = [3]
    transformer["from_node"] = [2]
    transformer["to_node"] = [4]
    transformer["from_status"] = [1]
    transformer["to_status"] = [1]
    transformer["u1"] = [1e4]
    transformer["u2"] = [4e2]
    transformer["sn"] = [1e5]
    transformer["uk"] = [0.1]
    transformer["pk"] = [1e3]
    transformer["i0"] = [1.0e-6]
    transformer["p0"] = [0.1]
    transformer["winding_from"] = [2]
    transformer["winding_to"] = [1]
    transformer["clock"] = [5]
    transformer["tap_side"] = [0]
    transformer["tap_pos"] = [3]
    transformer["tap_min"] = [-11]
    transformer["tap_max"] = [9]
    transformer["tap_size"] = [100]

    lv_feeders = [5]

    with pytest.raises(WrongFromNodeLVFeederError) as excinfo:
        # line
        line["from_node"] = [6, 4]
        line["to_node"] = [8, 6]
        # transformer
        transformer["from_node"] = [2]
        transformer["to_node"] = [4]
        # all
        input_data = {"node": node, "line": line, "sym_load": sym_load, "source": source, "transformer": transformer}
        PowerSim(grid_data=input_data, lv_feeders=lv_feeders)
    assert str(excinfo.value) == "The LV Feeder from_node does not correspond with the transformer to_node"

    with pytest.raises(WrongFromNodeLVFeederError) as excinfo:
        # line
        line["from_node"] = [4, 4]
        line["to_node"] = [6, 8]
        # transformer
        transformer["from_node"] = [2]
        transformer["to_node"] = [8]
        # all
        input_data = {"node": node, "line": line, "sym_load": sym_load, "source": source, "transformer": transformer}
        PowerSim(grid_data=input_data, lv_feeders=lv_feeders)
    assert str(excinfo.value) == "The LV Feeder from_node does not correspond with the transformer to_node"


def test_CycleError():

    # node
    node = initialize_array("input", "node", 3)
    node["id"] = [2, 4, 6]
    node["u_rated"] = [4e2, 4e2, 4e2]

    # load
    sym_load = initialize_array("input", "sym_load", 1)
    sym_load["id"] = [7]
    sym_load["node"] = [6]
    sym_load["status"] = [1]
    sym_load["type"] = [LoadGenType.const_power]
    sym_load["p_specified"] = [1e3]
    sym_load["q_specified"] = [5e3]

    # line
    line = initialize_array("input", "line", 2)
    line["id"] = [5, 20]
    line["from_node"] = [4, 2]
    line["to_node"] = [6, 6]
    line["from_status"] = [1, 1]
    line["to_status"] = [1, 1]
    line["r1"] = [10.0, 10.0]
    line["x1"] = [0.0, 0.0]
    line["c1"] = [0.0, 0.0]
    line["tan1"] = [0.0, 0.0]

    # source
    source = initialize_array("input", "source", 1)
    source["id"] = [1]
    source["node"] = [2]
    source["status"] = [1]
    source["u_ref"] = [1.0]

    # transformer
    transformer = initialize_array("input", "transformer", 1)
    transformer["id"] = [3]
    transformer["from_node"] = [2]
    transformer["to_node"] = [4]
    transformer["from_status"] = [1]
    transformer["to_status"] = [1]
    transformer["u1"] = [1e4]
    transformer["u2"] = [4e2]
    transformer["sn"] = [1e5]
    transformer["uk"] = [0.1]
    transformer["pk"] = [1e3]
    transformer["i0"] = [1.0e-6]
    transformer["p0"] = [0.1]
    transformer["winding_from"] = [2]
    transformer["winding_to"] = [1]
    transformer["clock"] = [5]
    transformer["tap_side"] = [0]
    transformer["tap_pos"] = [3]
    transformer["tap_min"] = [-11]
    transformer["tap_max"] = [9]
    transformer["tap_size"] = [100]
    # all
    input_data = {"node": node, "line": line, "sym_load": sym_load, "source": source, "transformer": transformer}

    lv_feeders = [5]

    with pytest.raises(GraphCycleError) as excinfo:
        PowerSim(grid_data=input_data, lv_feeders=lv_feeders)
    assert str(excinfo.value) == "Cycle found"

def test_GraphNotFullyConnectedError():

    # node
    node = initialize_array("input", "node", 4)
    node["id"] = [2, 4, 6, 45]
    node["u_rated"] = [1e4, 4e2, 4e2, 6e2]

    # load
    sym_load = initialize_array("input", "sym_load", 1)
    sym_load["id"] = [7]
    sym_load["node"] = [6]
    sym_load["status"] = [1]
    sym_load["type"] = [LoadGenType.const_power]
    sym_load["p_specified"] = [1e3]
    sym_load["q_specified"] = [5e3]

    # line
    line = initialize_array("input", "line", 1)
    line["id"] = [5]
    line["from_node"] = [4]
    line["to_node"] = [6]
    line["from_status"] = [1]
    line["to_status"] = [1]
    line["r1"] = [10.0]
    line["x1"] = [0.0]
    line["c1"] = [0.0]
    line["tan1"] = [0.0]

    # source
    source = initialize_array("input", "source", 1)
    source["id"] = [1]
    source["node"] = [2]
    source["status"] = [1]
    source["u_ref"] = [1.0]

    # transformer
    transformer = initialize_array("input", "transformer", 1)
    transformer["id"] = [3]
    transformer["from_node"] = [2]
    transformer["to_node"] = [4]
    transformer["from_status"] = [1]
    transformer["to_status"] = [1]
    transformer["u1"] = [1e4]
    transformer["u2"] = [4e2]
    transformer["sn"] = [1e5]
    transformer["uk"] = [0.1]
    transformer["pk"] = [1e3]
    transformer["i0"] = [1.0e-6]
    transformer["p0"] = [0.1]
    transformer["winding_from"] = [2]
    transformer["winding_to"] = [1]
    transformer["clock"] = [5]
    transformer["tap_side"] = [0]
    transformer["tap_pos"] = [3]
    transformer["tap_min"] = [-11]
    transformer["tap_max"] = [9]
    transformer["tap_size"] = [100]
    # all
    input_data = {"node": node, "line": line, "sym_load": sym_load, "source": source, "transformer": transformer}

    lv_feeders = [5]

    with pytest.raises(GraphNotFullyConnectedError) as excinfo:
        PowerSim(grid_data=input_data, lv_feeders=lv_feeders)
    assert str(excinfo.value) == "Graph not fully connected. Cannot reach all vertices."

class TestPowerSystemExceptions(unittest.TestCase):

    def setUp(self):
        # Load data from input_network_data.json
        self.grid_data = json_deserialize_from_file("src/power_system_simulation/input_network_data_2.json")

        # Load the Active Power Profile file
        try:
            self.active_power_profile = pd.read_parquet("src/power_system_simulation/active_power_profile_2.parquet")
        except FileNotFoundError:
            self.fail(
                "Active Power Profile file not found. Please ensure 'active_power_profile.parquet' is in the correct location."
            )

        # Load the Reactive Power Profile file
        try:
            self.reactive_power_profile = pd.read_parquet("src/power_system_simulation/reactive_power_profile_2.parquet")
        except FileNotFoundError:
            self.fail(
                "Reactive Power Profile file not found. Please ensure 'reactive_power_profile.parquet' is in the correct location."
            )
    
        # Load the Active Power Profile file
        try:
            self.EV_pool = pd.read_parquet("src/power_system_simulation/ev_active_power_profile_2.parquet")
        except FileNotFoundError:
            self.fail(
                "Active Power Profile file not found. Please ensure 'active_power_profile.parquet' is in the correct location."
            )

        # Instantiate the PowerFlow class with test data and power profiles
        self.pf = pss.PowerSim(grid_data=self.grid_data)

    def test_batch_powerflow(self):
        output_data = self.pf.batch_powerflow(self.active_power_profile, self.reactive_power_profile)
        self.assertIsInstance(output_data, dict)

        # Optionally, if there are specific expected outputs for the batch power flow,
        # those can be compared here as well. For now, we assume output_data validation
        # is done through the other methods.

    def test_no_active_power_profile(self):
        with self.assertRaises(pfp.PowerProfileNotFound):
            self.pf.batch_powerflow(None, self.reactive_power_profile)

    def test_no_reactive_power_profile(self):
        with self.assertRaises(pfp.PowerProfileNotFound):
            self.pf.batch_powerflow(self.active_power_profile, None)

    def test_timestamp_mismatch(self):
        reactive_power_profile = self.reactive_power_profile.copy()
        # Ensure the reactive power profile has a different number of timestamps
        reactive_power_profile.index = pd.date_range(
            start="2024-06-01", periods=len(self.reactive_power_profile), freq="h"
        )
        with self.assertRaises(pfp.TimestampMismatch):
            self.pf.batch_powerflow(self.active_power_profile, reactive_power_profile)

    def test_load_id_mismatch(self):
        reactive_power_profile = self.reactive_power_profile.copy()
        # Ensure the reactive power profile has different load IDs but same number of columns
        columns = reactive_power_profile.columns.tolist()
        columns[0] = "new_load_id"
        reactive_power_profile.columns = columns
        with self.assertRaises(pfp.LoadIDMismatch):
            self.pf.batch_powerflow(self.active_power_profile, reactive_power_profile)