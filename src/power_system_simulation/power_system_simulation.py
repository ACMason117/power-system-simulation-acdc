import numpy as np
import pandas as pd

import power_system_simulation.graph_processing as gp
import power_system_simulation.power_flow_processing as pfp

# write exceptions here


class TotalEnergyLoss:
    pass


class VoltageDeviation:
    pass


class PowerSim:
    def __init__(self, grid_data: dict) -> None:
        self.PowerSimModel = pfp.PowerFlow(grid_data=grid_data)

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

    def ev_penetration():
        pass

    def optimal_tap_position(
        self, active_power_profile: pd.DataFrame, reactive_power_profile: pd.DataFrame, opt_criteria=TotalEnergyLoss
    ) -> int:
        grid_data = self.PowerSimModel.grid_data

        update_tap = range(grid_data["transformer"]["tap_max"][0], grid_data["transformer"]["tap_min"][0] + 1)

        energy_loss_aggregate = {}
        voltage_deviation = {}
        voltage_table = {}

        # may god help us with this function
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
