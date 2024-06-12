import math
import random
import pandas as pd
import power_flow_processing as pfp


def process_evs(number_of_houses, number_of_feeders, penetration_level):
    # Calculate the total number of EVs and the number per feeder
    total_evs = number_of_houses * penetration_level
    evs_per_feeder = math.floor(total_evs / number_of_feeders)
    print(f"EVs per feeder: {evs_per_feeder}")


    # import data
    from power_grid_model.utils import json_deserialize_from_file

    grid_data = json_deserialize_from_file("input_network_data.json")
    active_power_profile = pd.read_parquet("active_power_profile.parquet")
    reactive_power_profile = pd.read_parquet("reactive_power_profile.parquet")
    pgm = pfp.PowerFlow(grid_data)
    pfp.assert_valid_input_data(input_data=grid_data, symmetric=True, calculation_type=pfp.CalculationType.power_flow)
    print(pgm)
    print(active_power_profile)
    # Randomly select houses for EV assignment within each feeder

    # these values should be given as an input from another file

    # Within a LV feeder, randomly select houses which will have EVs

    # For each selected house with EV, randomly select an EV charging profile to add to the sym_load of that house.

    # After assignment of EV profiles, run a time-series power flow as in Assignment 2, return the two aggregation tables.

    return evs_per_feeder