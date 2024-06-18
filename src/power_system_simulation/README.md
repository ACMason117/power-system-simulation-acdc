# power-system-simulation-ac/dc

This is a student project for Power System Simulation.

# Assignment 1
`graph_processing.py` contains the class `GraphProcessor`. 

This class defines and validates a grid and runs processing functions. It is initialized with parameters:
`def __init__(`
        `self,`
        `vertex_ids: List[int],`
        `edge_ids: List[int],`
        `edge_vertex_id_pairs: List[Tuple[int, int]],`
        `edge_enabled: List[bool],`
        `source_vertex_id: int,`
    `) -> None`

The object saves:
1. `self.vertex_ids`
2. `self.edge_ids`
3. `self.edge_vertex_id_pairs`
4. `self.edge_enabled`
5. `self.source_vertex_id`

The class contains the functions: 
1. `dfs(self, adjacency_list, visited, parent, parent_list, start_node) -> List[int]`
2. `build_adjacency_list(self, edge_vertex_id_pairs, edge_enabled)`
3. `find_downstream_vertices(self, edge_id: int) -> List[int]`
4. `find_alternative_edges(self, disabled_edge_id: int) -> List[int]`
5. `graph_plotter(self, plot_criteria=EnabledEdges) -> None`
6. `sort_tuple_list(edge_vertex_id_pairs) -> List[Tuple[int, int]]`



# Assignment 2
`power_flow_processing.py` contains the class `PowerFlow`. 
This class defines and validates a grid based on `power_grid_model.PowerGridModel`

It is initialized with parameters:
`def __init__(self, grid_data: dict) -> None`

`grid_data` must be provided in `power_grid_model` format. Refer to: 
https://power-grid-model.readthedocs.io/en/stable/quickstart.html#input-data

The object saves:
1. `self.model`
2. `self.grid_data`

The class contains the functions: 
1. `batch_powerflow(`
   `self, active_power_profile: pd.DataFrame, reactive_power_profile: pd.DataFrame, tap_value=0`
   `) -> dict`
2. `aggregate_voltage_table(`
   `self, active_power_profile: pd.DataFrame, reactive_power_profile: pd.DataFrame`
   `) -> pd.DataFrame`
3. `aggregate_loading_table(`
   `self, active_power_profile: pd.DataFrame, reactive_power_profile: pd.DataFrame, tap_value=0`
   `) -> pd.DataFrame`


# Assignment 3
`power_system_simulation.py` contains the class `PowerSim`. 
This class defines and validates a grid based on `power_flow_processing.PowerFlow`

It is initialized with parameters:
`def __init__(`
`self,`
`grid_data: dict,`
`lv_feeders: list = None,`
`active_power_profile: pd.DataFrame = None,`
`reactive_power_profile: pd.DataFrame = None,`
`) -> None`

The object saves:
`self.power_sim_model = pfp.PowerFlow(grid_data=grid_data)`
`self.grid_data`
`self.lv_feeders`
`self.active_power_profile`
`self.reactive_power_profile`

This data is used if no input is provided to the class functions.

The class contains the functions: 
1. `n1_calculations(`
   `self,`
   `grid_data: dict,`
   `active_power_profile: pd.DataFrame,`
   `reactive_power_profile: pd.DataFrame,`
   `disabled_edge_id: int,`
   `) -> pd.DataFrame`
2. `ev_penetration(`
   `self,`
   `num_houses: int,`
   `num_feeders: int,`
   `penetration_level: float,`
   `active_power_profile: pd.DataFrame,`
   `reactive_power_profile: pd.DataFrame,`
   `ev_active_power_profile: pd.DataFrame,`
   `) -> tuple`
3. `optimal_tap_position(`
   `self,`
   `active_power_profile: pd.DataFrame = None,`
   `reactive_power_profile: pd.DataFrame = None,`
   `opt_criteria=TotalEnergyLoss,`
   `) -> int`
4. `network_plotter(self, plot_criteria=graph_processing.EnabledEdges) -> None`