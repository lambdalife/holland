import random
import numpy as np


def get_uniform_crossover_function():
    """
    Returns a function that applies uniform crossover (each gene value is chosen at random from the parent genes); see :ref:`crossover-functions`

    :Valid For:
        any gene type

    
    :returns: a function that accepts a list of parent genes and applies uniform crossover to them and returns a new gene
    """

    def uniform_crossover(parent_genes):
        if type(parent_genes[0]) != list:
            return random.choice(parent_genes)
        return [random.choice(options) for options in zip(*parent_genes)]

    return uniform_crossover


def get_point_crossover_function(n_crossover_points=1):
    """
    Returns a function that applies point crossover (take gene values from one parent gene at a time until reaching a crossover point, then switch parent genes); see :ref:`crossover-functions`

    :Valid For:
        any list-type gene
    
    :param n_crossover_points: number of points at which to switch to the next parent gene (should be at least ``len(parent_genes) - 1``)
    :type n_crossover_points: int
    

    :returns: a function that accepts a list of parent genes and applies point crossover


    :raises ValueError: if ``n_crossover_points`` is negative
    """
    if n_crossover_points < 0:
        raise ValueError("Number of crossover points cannot be negative")

    def point_crossover(parent_genes):
        crossover_points = sorted(
            np.random.choice(range(1, len(parent_genes[0])), size=n_crossover_points)
        )
        crossover_points.insert(0, 0)
        crossover_points.append(len(parent_genes[0]))

        offspring = []
        current_parent_index = 0
        for start, end in zip(crossover_points, crossover_points[1:]):
            offspring += parent_genes[current_parent_index][start:end]
            current_parent_index = (current_parent_index + 1) % len(parent_genes)
        return offspring

    return point_crossover


def get_and_crossover_function():
    """
    Returns a function that reduces the values of the parent_genes by the logical 'and' operation; see :ref:`crossover-functions`
    
    :Valid For:
        ``"bool"`` and ``"[bool]"`` gene types


    :returns: a function that accepts a list of parent genes and applies 'and' crossover
    """

    def and_crossover(parent_genes):
        if isinstance(parent_genes[0], list):
            size = len(parent_genes[0])
            return [all(pg[i] for pg in parent_genes) for i in range(size)]
        return all(parent_genes)

    return and_crossover


def get_or_crossover_function():
    """
    Returns a function that reduces the values of the parent_genes by the logical 'or' operation; see :ref:`crossover-functions`

    :Valid For:
        ``"bool"`` and ``"[bool]"`` gene types


    :returns: a function that accepts a list of parent genes and applies 'or' crossover
    """

    def or_crossover(parent_genes):
        if isinstance(parent_genes[0], list):
            size = len(parent_genes[0])
            return [any(pg[i] for pg in parent_genes) for i in range(size)]
        return any(parent_genes)

    return or_crossover
