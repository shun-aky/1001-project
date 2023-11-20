from enum import Enum

DISTANCE_THRESHOLD_CM = 30.0

class Recognition(Enum):
    FIRST_SUCCESS = 0
    FIRST_FAILURE = 1
    SECOND_SUCCESS = 2
    SECOND_FAILURE = 3

PIN_1 = 1
