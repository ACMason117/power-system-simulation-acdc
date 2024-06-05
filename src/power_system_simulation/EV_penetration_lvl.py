import math
import random


def process_evs(number_of_houses, number_of_feeders, penetration_level):
    # Calculate the total number of EVs and the number per feeder
    total_evs = number_of_houses * penetration_level
    evs_per_feeder = math.floor(total_evs / number_of_feeders)
    print(f"EVs per feeder: {evs_per_feeder}")

    # Randomly select houses for EV assignment within each feeder

    # these values should be given as an input from another file

    # Within a LV feeder, randomly select houses which will have EVs

    # For each selected house with EV, randomly select an EV charging profile to add to the sym_load of that house.

    # After assignment of EV profiles, run a time-series power flow as in Assignment 2, return the two aggregation tables.

    return evs_per_feeder
