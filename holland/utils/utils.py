import numpy as np


def bound_value(value, minimum=None, maximum=None):
    if minimum is None:
        minimum = -np.inf
    if maximum is None:
        maximum = np.inf
    return min(max(value, minimum), maximum)
