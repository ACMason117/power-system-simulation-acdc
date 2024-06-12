import math
import pandas as pd
import power_flow_processing as pfp

class PowerSim:
    def __init__(self, grid_data: dict) -> None:
        self.PowerSimModel = pfp.PowerFlow(grid_data=grid_data)
        print(grid_data)

    def example_code(self):
        print("Who reads trek een bak")

    def n1_calculations(self):
        pass

    def ev_penetration(self, number_of_houses, number_of_feeders, penetration_level):
        # Calculate the total number of EVs and the number per feeder
        total_evs = number_of_houses * penetration_level
        evs_per_feeder = math.floor(total_evs / number_of_feeders)
        print(f"EVs per feeder: {evs_per_feeder}")

        # Import data
        from power_grid_model.utils import json_deserialize_from_file

        grid_data = json_deserialize_from_file("input_network_data.json")
        active_power_profile = pd.read_parquet("active_power_profile.parquet")
        reactive_power_profile = pd.read_parquet("reactive_power_profile.parquet")
        pgm = pfp.PowerFlow(grid_data)
        pfp.assert_valid_input_data(input_data=grid_data, symmetric=True, calculation_type=pfp.CalculationType.power_flow)
        print(pgm)
        print(active_power_profile)
        
        # Randomly select houses for EV assignment within each feeder

        # Within a LV feeder, randomly select houses which will have EVs

        # For each selected house with EV, randomly select an EV charging profile to add to the sym_load of that house.

        # After assignment of EV profiles, run a time-series power flow as in Assignment 2, return the two aggregation tables.

        return evs_per_feeder

    def optimal_tap_position(self):
        pass
# Example usage:
# grid_data = some_function_to_load_grid_data()
# sim = PowerSim(grid_data)
# evs_per_feeder = sim.ev_penetration(150, 7, 0.20)
