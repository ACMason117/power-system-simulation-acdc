import math

import graph_processing as gp
import numpy as np
import pandas as pd
import power_flow_processing as pfp

# write exceptions here


class TotalEnergyLoss:
    pass


class VoltageDeviation:
    pass


class PowerSim:
    def __init__(self, grid_data: dict) -> None:
        self.PowerSimModel = pfp.PowerFlow(grid_data=grid_data)

    def example_code(self):
        print("Who reads trek een bak")

    def n1_calculations():

        pass

    def ev_penetration(
        self,
        num_houses: int,
        num_feeders: int,
        penetration_level: int,
        active_power_profile: pd.DataFrame,
        reactive_power_profile: pd.DataFrame,
        ev_active_power_profile: pd.DataFrame,
    ) -> int:
        # Randomly select houses for EV assignment within each feeder
        # These values should be given as an input from another file
        # Within a LV feeder, randomly select houses which will have EVs
        # For each selected house with EV, randomly select an EV charging profile to add to the sym_load of that house.
        # After assignment of EV profiles, run a time-series power flow as in Assignment 2, return the two aggregation tables.

        # data setup
        grid_data = self.PowerSimModel.grid_data

        total_evs = num_houses * penetration_level
        evs_per_feeder = math.floor(total_evs / num_feeders)
        print(f"EVs per feeder: {evs_per_feeder}")

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
        test4 = gp.GraphProcessor(
            vertex_ids=vertex_ids,
            edge_ids=edge_ids,
            edge_vertex_id_pairs=edge_vertex_id_pairs,
            edge_enabled=edge_enabled,
            source_vertex_id=source_vertex_id,
        )
        transformer_to_node = grid_data["transformer"][0]["to_node"]

        # assigned_profiles = set()   # This keeps track of the assigned profiles

        for line in grid_data["line"]:
            if line["from_node"] == transformer_to_node:
                print(f"Found line with from_node {transformer_to_node}: to_node = {line['to_node']}")
                print(f"Edge details: id = {line['id']}, r1 = {line['r1']}, x1 = {line['x1']}, ...")  # Find all feeders
                downstream_vertices = test4.find_downstream_vertices(line["id"])
                # print(downstream_vertices)
                sym_load_nodes = set(grid_data["sym_load"]["node"])
                common_nodes = sym_load_nodes.intersection(downstream_vertices)
                print(common_nodes)  # all the nodes in a downstream vertex that have a sym load
                
        combined_profile = active_power_profile
        # combined_profile[symload_id] = active_power_profile[symload_id].values + ev_active_power_profile[ev_id].values  

    def optimal_tap_position(
        self, active_power_profile: pd.DataFrame, reactive_power_profile: pd.DataFrame, opt_criteria=TotalEnergyLoss
    ) -> int:
        grid_data = self.PowerSimModel.grid_data

        update_tap = range(grid_data["transformer"]["tap_max"][0], grid_data["transformer"]["tap_min"][0] + 1)

        energy_loss_aggregate = {}
        voltage_deviation = {}
        voltage_table = {}

        for i in update_tap:
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
