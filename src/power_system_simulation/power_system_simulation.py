import math
import random

import numpy as np
import pandas as pd

try:
    import graph_processing as gp
    import power_flow_processing as pfp
except:
    import power_system_simulation.graph_processing as gp
    import power_system_simulation.power_flow_processing as pfp


# write exceptions here
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


class NotEnoughHousesForEVassignment(Exception):
    """Raises error if there are not enough houses to assign EV profiles to

    Args:
        Exception: _description_
    """


class NotEnoughEVprofilesForHouseAssignment(Exception):
    """Raises error if there are not enough EV profiles to assign to all houses

    Args:
        Exception: _description_
    """


class TotalEnergyLoss:
    pass


class VoltageDeviation:
    pass


class PowerSim:
    def __init__(
        self,
        grid_data: dict,
        lv_feeders: list = None,
        active_power_profile: pd.DataFrame = None,
        reactive_power_profile: pd.DataFrame = None,
    ) -> None:
        self.PowerSimModel = pfp.PowerFlow(grid_data=grid_data)

        self.grid_data = grid_data
        self.lv_feeders = lv_feeders
        self.active_power_profile = active_power_profile
        self.reactive_power_profile = reactive_power_profile
        # self.EV_pool=EV_pool

        # Check if there is exactly one source
        if len(grid_data["source"]) != 1:
            raise NotExactlyOneSourceError("There is not exactly one source")

        # Check if there is exactly one transformer
        if len(grid_data["transformer"]) != 1:
            raise NotExactlyOneTransformerError("There is not exactly one transformer")

        # Check if the LV feeder IDs are valid line IDs
        if self.lv_feeders is not None:
            for i in self.lv_feeders:
                if i not in self.grid_data["line"]["id"]:
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
        edge_enabled = []
        for i in grid_data["line"]["id"]:
            index = np.where(grid_data["line"]["id"] == i)
            if grid_data["line"][index]["from_status"] == 1 & grid_data["line"][index]["to_status"] == 1:
                edge_enabled = edge_enabled + [True]
            else:
                edge_enabled = edge_enabled + [False]
        if grid_data["transformer"][0]["from_status"] == 1 & grid_data["transformer"][0]["to_status"] == 1:
            edge_enabled = edge_enabled + [True]
        else:
            edge_enabled = edge_enabled + [False]
        source_vertex_id = grid_data["source"]["node"][0]
        edge_ids = list(grid_data["line"]["id"]) + list(grid_data["transformer"]["id"])
        vertex_ids = grid_data["node"]["id"]

        self.graph = gp.GraphProcessor(vertex_ids, edge_ids, edge_vertex_id_pairs, edge_enabled, source_vertex_id)

    def n1_calculations(
        self,
        grid_data: dict,
        active_power_profile: pd.DataFrame,
        reactive_power_profile: pd.DataFrame,
        disabled_edge_id: int,
    ) -> pd.DataFrame:

        # Rewriting the grid dataframe to assignment 1 list:

        edge_vertex_id_pairs = list(zip(grid_data["line"]["from_node"], grid_data["line"]["to_node"])) + list(
            zip(grid_data["transformer"]["from_node"], grid_data["transformer"]["to_node"])
        )
        edge_enabled = []
        for i in grid_data["line"]["id"]:
            index = np.where(grid_data["line"]["id"] == i)
            if grid_data["line"][index]["from_status"] == 1 & grid_data["line"][index]["to_status"] == 1:
                edge_enabled = edge_enabled + [True]
            else:
                edge_enabled = edge_enabled + [False]
        if grid_data["transformer"][0]["from_status"] == 1 & grid_data["transformer"][0]["to_status"] == 1:
            edge_enabled = edge_enabled + [True]
        else:
            edge_enabled = edge_enabled + [False]
        source_vertex_id = grid_data["source"]["node"][0]
        edge_ids = list(grid_data["line"]["id"]) + list(grid_data["transformer"]["id"])
        vertex_ids = grid_data["node"]["id"]

        # Find alternative edges

        graph = gp.GraphProcessor(
            vertex_ids=vertex_ids,
            edge_ids=edge_ids,
            edge_vertex_id_pairs=edge_vertex_id_pairs,
            edge_enabled=edge_enabled,
            source_vertex_id=source_vertex_id,
        )

        alt_edges = graph.find_alternative_edges(disabled_edge_id)

        # Run Powerflow table and aggregate table

        results = []

        line_data = grid_data["line"]

        for alt_line_id in alt_edges:
            alt_line_index = None
            for i in range(len(line_data["id"])):
                if line_data["id"][i] == alt_line_id:
                    alt_line_index = i
                    break
            if alt_line_index is not None:
                line_data["to_status"][alt_line_index] = 1
                loading_table = self.PowerSimModel.aggregate_loading_table(
                    active_power_profile=active_power_profile, reactive_power_profile=reactive_power_profile
                )

                max_loading = loading_table["Max_Loading"].max()
                max_loading_id = loading_table["Max_Loading"].idxmax()
                max_loading_timestamp = loading_table.loc[max_loading_id, "Max_Loading_Timestamp"]

                results.append(
                    {
                        "Alternative_Line_ID": alt_line_id,
                        "Max_Loading": max_loading,
                        "Max_Loading_ID": max_loading_id,
                        "Max_Loading_Timestamp": max_loading_timestamp,
                    }
                )
        results_df = pd.DataFrame(results)
        if results_df.empty:
            results_df = pd.DataFrame(
                columns=["Alternative_Line_ID", "Max_Loading", "Max_Loading_ID", "Max_Loading_Timestamp"]
            )

        return results_df

    def ev_penetration(
        self,
        num_houses: int,
        num_feeders: int,
        penetration_level: float,  # Changed to float to represent percentage
        active_power_profile: pd.DataFrame,
        reactive_power_profile: pd.DataFrame,
        ev_active_power_profile: pd.DataFrame,
    ) -> tuple:
        """
        Assign EV charging profiles based on penetration level and run power flow analysis.

        Args:
            num_houses (int): Number of houses in the grid.
            num_feeders (int): Number of feeders in the grid.
            penetration_level (float): Percentage of houses with EV charging.
            active_power_profile (pd.DataFrame): Active power profile for houses.
            reactive_power_profile (pd.DataFrame): Reactive power profile for houses.
            ev_active_power_profile (pd.DataFrame): EV charging profiles.

        Returns:
            tuple: Aggregated voltage and loading tables.
        """

        # Calculate number of EVs per feeder
        total_evs = math.floor(penetration_level * num_houses / 100)
        evs_per_feeder = math.floor(total_evs / num_feeders)

        grid_data = self.grid_data  # Assuming grid_data is an attribute of self

        # Initialize the GraphProcessor to find downstream vertices
        edge_vertex_id_pairs = list(zip(grid_data["line"]["from_node"], grid_data["line"]["to_node"])) + list(
            zip(grid_data["transformer"]["from_node"], grid_data["transformer"]["to_node"])
        )
        edge_enabled = [
            (f_status == 1 and t_status == 1)
            for f_status, t_status in zip(grid_data["line"]["from_status"], grid_data["line"]["to_status"])
        ]
        edge_enabled += [
            (grid_data["transformer"]["from_status"][0] == 1 and grid_data["transformer"]["to_status"][0] == 1)
        ]
        source_vertex_id = grid_data["source"]["node"][0]
        edge_ids = list(grid_data["line"]["id"]) + list(grid_data["transformer"]["id"])
        vertex_ids = grid_data["node"]["id"]

        test4 = gp.GraphProcessor(
            vertex_ids=vertex_ids,
            edge_ids=edge_ids,
            edge_vertex_id_pairs=edge_vertex_id_pairs,
            edge_enabled=edge_enabled,
            source_vertex_id=source_vertex_id,
        )

        transformer_to_node = grid_data["transformer"]["to_node"][0]

        assigned_profiles = set()
        for line in grid_data["line"]:
            if line["from_node"] == transformer_to_node:
                downstream_vertices = test4.find_downstream_vertices(line["id"])
                sym_load_nodes = set(grid_data["sym_load"]["node"])
                common_nodes = sym_load_nodes.intersection(downstream_vertices)

                common_nodes_list = sorted(common_nodes)

                # Check if the number of EVs per feeder is greater than the available houses
                if len(common_nodes_list) < evs_per_feeder:
                    evs_per_feeder = len(common_nodes_list)

                selected_houses = random.sample(common_nodes_list, evs_per_feeder)

                available_ev_profiles = list(set(ev_active_power_profile.columns) - assigned_profiles)
                selected_ev_profiles = random.sample(available_ev_profiles, evs_per_feeder)
                assigned_profiles.update(selected_ev_profiles)

                # Ensure the house and EV profile are present in the respective DataFrames
                for house, ev_profile in zip(selected_houses, selected_ev_profiles):
                    if house in active_power_profile.columns and ev_profile in ev_active_power_profile.columns:
                        active_power_profile[house] += ev_active_power_profile[ev_profile]

        # Run time-series power flow after assigning EV profiles
        self.grid_data = grid_data  # Update grid data with new sym_load values if needed
        voltage_table = self.PowerSimModel.aggregate_voltage_table(active_power_profile, reactive_power_profile)
        loading_table = self.PowerSimModel.aggregate_loading_table(active_power_profile, reactive_power_profile)

        return voltage_table, loading_table

    def optimal_tap_position(
        self,
        active_power_profile: pd.DataFrame = None,
        reactive_power_profile: pd.DataFrame = None,
        opt_criteria=TotalEnergyLoss,
    ) -> int:

        if active_power_profile is None:
            active_power_profile = self.active_power_profile

        if reactive_power_profile is None:
            reactive_power_profile = self.reactive_power_profile

        grid_data = self.PowerSimModel.grid_data

        update_tap = range(grid_data["transformer"]["tap_max"][0], grid_data["transformer"]["tap_min"][0] + 1)

        energy_loss_aggregate = {}
        voltage_deviation = {}
        voltage_table = {}

        # output_data = {}

        for i in update_tap:
            # output_data[f"tap{i}"] = self.PowerSimModel.batch_powerflow(
            #     active_power_profile=active_power_profile, reactive_power_profile=reactive_power_profile, tap_value=i
            # )

            if opt_criteria == TotalEnergyLoss:
                energy_loss_aggregate[f"{i}"] = sum(
                    (
                        self.PowerSimModel.aggregate_loading_table(
                            active_power_profile=active_power_profile,
                            reactive_power_profile=reactive_power_profile,
                            tap_value=i,
                        )
                    )["Total_Loss"]
                )

            elif opt_criteria == VoltageDeviation:
                voltage_table[f"{i}"] = self.PowerSimModel.aggregate_voltage_table(
                    active_power_profile=active_power_profile, reactive_power_profile=reactive_power_profile
                )
                voltage_deviation[f"{i}"] = sum(
                    (pd.DataFrame(voltage_table[f"{i}"][["Max_Voltage", "Min_Voltage"]] - 1).max(axis=1)).tolist()
                ) / len((pd.DataFrame(voltage_table[f"{i}"][["Max_Voltage", "Min_Voltage"]] - 1).max(axis=1)).tolist())

        if opt_criteria == TotalEnergyLoss:
            optimal_tap = int(min(energy_loss_aggregate, key=lambda k: energy_loss_aggregate[k]))

        elif opt_criteria == VoltageDeviation:
            # print(pd.DataFrame(voltage_deviation.keys()))
            optimal_tap = int(min(voltage_deviation, key=lambda k: voltage_deviation[k]))
            # print(optimal_tap)

        return optimal_tap
