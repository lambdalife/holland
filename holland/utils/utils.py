import re
import math
import numpy as np


def bound_value(value, minimum=-np.inf, maximum=np.inf):
    """
    Bounds a value between a minimum and maximum

    :param value: the value to bound
    :type value: int/float

    :param minimum: the lower bound
    :type minimum: int/float

    :param maximum: the upper bound
    :type maximum: int/float


    :returns: the bounded value
    """
    if minimum is None:  # in case None is passed in
        minimum = -np.inf
    if maximum is None:
        maximum = np.inf
    return min(max(value, minimum), maximum)


def select_from(values, top=0, mid=0, bottom=0, random=0):
    """
    Selects elements from a (sorted) list without replacement

    :param values: the list of values to select from
    :type values: list

    :param top: number of elements to select from the top (end) of the list
    :type top: int

    :param mid: number of elements to select from the middle of the list
    :type mid: int

    :param bottom: number of elements to select from the bottom (start) of the list
    :type bottom: int

    :param random: number of elements to select randomly from the list
    :type random: int


    :returns: a list of selected elements
    """
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
    random_ids = np.random.choice(remaining_ids, replace=False, size=random)
    selected += [values[i] for i in random_ids]

    return selected


def is_numeric_type(gene_params):
    """
    Determines if a gene is of a numeric type or not (whether list type or not); e.g. returns ``False`` if type is ``"bool"`` or ``"[bool]"``, but ``True`` if type is ``"float"`` or ``"[float]"``

    :param gene_params: a dictionary of parameters for a single gene; see :ref:`genome-params`
    :type gene_params: dict

    :returns: a boolean indiciating whether the gene is of a numeric type or not
    """
    if is_list_type(gene_params):
        value_type = re.findall(r"\[(.+?)\]", gene_params["type"])[0]
    else:
        value_type = gene_params["type"]

    return value_type in ["int", "float"]


def is_list_type(gene_params):
    """
    Determines if a gene is of a list type or not; e.g. returns ``False`` if type is ``"float"`` but ``True`` if type is ``"[float]"``

    :param gene_params: a dictionary of parameters for a single gene; see :ref:`genome-params`
    :type gene_params: dict

    :returns: a boolean indicating whether the gene is of a list type or not
    """
    return re.match(r"\[.+?\]", gene_params["type"])
