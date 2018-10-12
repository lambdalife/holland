import re
import math
import numpy as np


def bound_value(value, minimum=-math.inf, maximum=math.inf, to_int=False):
    """
    Bounds a value between a minimum and maximum

    :param value: the value to bound
    :type value: int/float

    :param minimum: the lower bound
    :type minimum: int/float

    :param maximum: the upper bound
    :type maximum: int/float

    :param to_int: whether or not to cast the result to an int
    :type to_int: bool


    :returns: the bounded value
    """
    if minimum is None:  # in case None is passed in
        minimum = -math.inf
    if maximum is None:
        maximum = math.inf
    if to_int:
        if isinstance(minimum, float) and minimum != -math.inf:
            return int(min(max(value, math.ceil(minimum)), maximum))
        return int(min(max(value, minimum), maximum))
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

    remaining_values = values[bottom:middle_start_index] + values[middle_start_index + mid : -top]
    selected += select_random(remaining_values, n=random)

    return selected


def select_random(choices, probabilities=None, n=1, should_replace=False):
    """
    Selects random elements from a list

    :param choices: list of elements to select from
    :type choices: list

    :param probabilities: list of probabilities for selecting each element in ``choices``; if not specified, uniform probability is used
    :type probabilities: list

    :param n: number of elements to select from ``choices``
    :type n: int

    :param should_replace: specifies if selection should be done with replacement or not
    :type should_replace: bool


    :returns: a list of length ``n`` of elements selected randomly from ``choices``

    
    :raises ValueError: if ``probabilities`` is given but ``len(probabilities) != len(choices)``
    :raises ValueError: if any element of ``probabilities`` is negative
    :raises ValueError: if ``sum(probabilities) > 1``
    :raises ValueError: if ``should_replace`` is ``False`` but ``n > len(choices)``
    """
    if probabilities is not None:
        if len(probabilities) != len(choices):
            raise ValueError("Number of probabilities must match number of choices")
        if any(p < 0 for p in probabilities):
            raise ValueError("Probabilities cannot be negative")
        if sum(probabilities) != 1:
            raise ValueError("Probabilities must sum to 1")
    if not should_replace and n > len(choices):
        raise ValueError(
            "Number of elements to select cannot exceed number of choices without replacement"
        )

    # temporary:
    if type(choices[0]) in [list, dict, tuple]:
        index_choices = range(len(choices))
        selected_indices = list(
            np.random.choice(index_choices, p=probabilities, size=n, replace=should_replace)
        )
        return [x for i, x in enumerate(choices) if i in selected_indices]

    return list(np.random.choice(choices, p=probabilities, size=n, replace=should_replace))


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
