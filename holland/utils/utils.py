import math
import numpy as np


def bound_value(value, minimum=-np.inf, maximum=np.inf):
    if minimum is None: # in case None is passed in
        minimum = -np.inf
    if maximum is None:
        maximum = np.inf
    return min(max(value, minimum), maximum)


def select_from(values, top=0, mid=0, bottom=0, random=0):
    if top + mid + bottom + random > len(values):
        raise ValueError("Cannot select more values than the number of values given")
    if any(param < 0 for param in (top, mid, bottom, random)):
        raise ValueError("Selection numbers cannot be negative")

    selected = []

    if len(values) % 2 == 0:
        middle_start_index = math.ceil(len(values) / 2) - math.floor(mid / 2)
    else:
        middle_start_index = math.ceil(len(values) / 2) - math.ceil(mid / 2)
    selected += values[-top:]
    selected += values[middle_start_index : middle_start_index + mid]
    selected += values[:bottom]

    # use ids because np.random.choice argument must be 1 dimensional
    all_ids = list(range(len(values)))
    remaining_ids = (
        all_ids[bottom:middle_start_index] + all_ids[middle_start_index + mid : -top]
    )
    random_ids = np.random.choice(remaining_ids, size=random)
    selected += [values[i] for i in random_ids]

    return selected
