"""Sample loss triangle data for commercial auto liability.

This triangle exhibits heterogeneous loss volumes across accident years,
with larger-volume years tending to develop more slowly due to the
increased complexity of claims in expanded underwriting periods.
"""

ORIGIN_LABELS = [
    "2014", "2015", "2016", "2017", "2018",
    "2019", "2020", "2021", "2022", "2023",
]

DEV_PERIODS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Cumulative incurred losses (thousands)
CUMULATIVE_DATA = [
    [3012, 5572, 7354, 8604, 9292, 9663, 9905, 10044, 10144, 10205],
    [8269, 12817, 16021, 18264, 19543, 20305, 20711, 20960, 21128],
    [3540, 6372, 8274, 9598, 10366, 10781, 11051, 11206],
    [7850, 12160, 15078, 17189, 18393, 19105, 19487],
    [3280, 5904, 7734, 9049, 9773, 10164],
    [8690, 13471, 16839, 19196, 20540],
    [3450, 6210, 8073, 9365],
    [7920, 12276, 15345],
    [3180, 5883],
    [8150],
]

# Earned premiums by accident year (thousands)
EARNED_PREMIUMS = [
    15700, 32200, 16300, 31000, 15500,
    33800, 14800, 31500, 15200, 33000,
]

EXPECTED_LOSS_RATIO = 0.65
