import math
import os

import graph_processing as tp
import pandas as pd
import power_flow_processing as pfp
from power_grid_model.utils import json_deserialize_from_file


def process_evs(number_of_houses, number_of_feeders, penetration_level):
    # Calculate the total number of EVs and the number per feeder
    total_evs = number_of_houses * penetration_level
    evs_per_feeder = math.floor(total_evs / number_of_feeders)
    print(f"EVs per feeder: {evs_per_feeder}")

    # Determine the file path relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    grid_data_path = os.path.join(script_dir, "Assigment3_data\input_network_data.json")
    active_power_profile_path = os.path.join(script_dir, "active_power_profile.parquet")
    reactive_power_profile_path = os.path.join(script_dir, "reactive_power_profile.parquet")

    # Import data
    grid_data = json_deserialize_from_file(grid_data_path)
    active_power_profile = pd.read_parquet(active_power_profile_path)
    reactive_power_profile = pd.read_parquet(reactive_power_profile_path)

    # Randomly select houses for EV assignment within each feeder
    # These values should be given as an input from another file
    # Within a LV feeder, randomly select houses which will have EVs
    # For each selected house with EV, randomly select an EV charging profile to add to the sym_load of that house.
    # After assignment of EV profiles, run a time-series power flow as in Assignment 2, return the two aggregation tables.
    pgm = pfp.PowerFlow(grid_data)
    return evs_per_feeder
