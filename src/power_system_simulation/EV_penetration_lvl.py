import math

# Inputs
NUMBER_OF_HOUSES = 150
NUMBER_OF_FEEDERS = 7
PENETRATION_LEVEL = 0.20

TOTAL_EVS = NUMBER_OF_HOUSES*PENETRATION_LEVEL
EVS_PER_FEEDER = math.floor(TOTAL_EVS / NUMBER_OF_FEEDERS) # this function rounds down the output to a whole number
print(EVS_PER_FEEDER)
# these values should be given as an input from another file

# Within a LV feeder, randomly select houses which will have EVs

# For each selected house with EV, randomly select an EV charging profile to add to the sym_load of that house.

# After assignment of EV profiles, run a time-series power flow as in Assignment 2, return the two aggregation tables.