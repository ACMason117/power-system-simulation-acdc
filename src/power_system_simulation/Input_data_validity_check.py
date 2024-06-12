import json
import pprint
import warnings

import numpy as np
import pandas as pd
import power_grid_model as pgm
import pyarrow as pa
import pyarrow.parquet as pq

with warnings.catch_warnings(action="ignore", category=DeprecationWarning):
    # suppress warning about pyarrow as future required dependency
    from pandas import DataFrame

from power_grid_model import CalculationMethod, CalculationType, PowerGridModel, initialize_array
from power_grid_model.utils import json_deserialize, json_serialize
from power_grid_model.validation import assert_valid_input_data
from pyarrow import table

from power_system_simulation.graph_processing import GraphCycleError, GraphNotFullyConnectedError, GraphProcessor
from power_system_simulation.power_flow_processing import PowerFlow


class NotExactlyOneSourceError(Exception):
    """Raises MoreThanOneSourceError if there is not exactly one source

    Args:
        Exception: _description_
    """


class NotExactlyOneTransformerError(Exception):
    """Raises MoreThanOneSourceError if there is not exactly one transformer

    Args:
        Exception: _description_
    """


class InvalidLVFeederIDError(Exception):
    """Raises InvalidLVFeederIDError if the LV feeder IDs are not valid line IDS

    Args:
        Exception: _description_
    """


class WrongFromNodeLVFeederError(Exception):
    """Raises WrongFromNodeLVFeederError if the LV feeder from_node does not correspond with the transformer to_node

    Args:
        Exception: _description_
    """


class validity_check:

    def __init__(
        self,
        grid_data: dict = None,
        lv_feeders: list = None,  # , active_power_profile: table = None, reactive_power_profile: table = None
    ) -> None:
        # , EV_pool: table = None
        assert_valid_input_data(input_data=grid_data, symmetric=True, calculation_type=CalculationType.power_flow)

        self.grid_data = grid_data
        self.lv_feeders = lv_feeders
        # self.active_power_profile = active_power_profile
        # self.reactive_power_profile = reactive_power_profile
        # self.EV_pool=EV_pool

        # Check if there is exactly one source
        if len(grid_data["source"]) != 1:
            raise NotExactlyOneSourceError("There is not exactly one source")

        # Check if there is exactly one transformer
        if len(grid_data["transformer"]) != 1:
            raise NotExactlyOneTransformerError("There is not exactly one transformer")

        # Check if the LV feeder IDs are valid line IDs
        for i in lv_feeders:
            if i not in grid_data["line"]["id"]:
                raise InvalidLVFeederIDError("LV feeder IDs are not valid line IDs")

        # Check if the lines in the LV Feeder IDs have the from_node the same as the to_node of the transformer
        for i in lv_feeders:
            index = np.where(grid_data["line"]["id"] == i)
            if grid_data["line"][index]["from_node"] != grid_data["transformer"][0]["to_node"]:
                raise WrongFromNodeLVFeederError(
                    "The LV Feeder from_node does not correspond with the transformer to_node"
                )

        # Check if the graph does not contain cycles
        edge_vertex_id_pairs = list(zip(grid_data["line"]["from_node"], grid_data["line"]["to_node"])) + list(
            zip(grid_data["transformer"]["from_node"], grid_data["transformer"]["to_node"])
        )
        print(edge_vertex_id_pairs)
        edge_enabled = []
        for i in grid_data["line"]["id"]:
            index = np.where(grid_data["line"]["id"] == i)
            if grid_data["line"][index]["from_status"] == 1 & grid_data["line"][index]["to_status"] == 1:
                edge_enabled = True
            else:
                edge_enabled = False
        # source_vertex_id=grid_data["source"]["id"]
        # vertex_ids=grid_data["line"]["id"]
        # vertex_visited = []
        # vertex_parents = {}
        # adjacency_list = GraphProcessor.build_adjacency_list(edge_vertex_id_pairs, edge_enabled)
        # if GraphProcessor.dfs(adjacency_list, vertex_visited, float("Nan"), vertex_parents, source_vertex_id) == 1:
        #    raise GraphCycleError("Cycle found")

        ## 7. The graph should be fully connected
        # if len(vertex_visited) != len(vertex_ids):
        #    raise GraphNotFullyConnectedError("Graph not fully connected. Cannot reach all vertices.")
