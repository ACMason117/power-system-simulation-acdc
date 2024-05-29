import math

# Inputs
NUMBER_OF_HOUSES = 150
NUMBER_OF_FEEDERS = 7
PENETRATION_LEVEL = 0.20

TOTAL_EVS = NUMBER_OF_HOUSES*PENETRATION_LEVEL
EVS_PER_FEEDER = math.floor(TOTAL_EVS / NUMBER_OF_FEEDERS) # this function rounds down the output to a whole number
print(EVS_PER_FEEDER)