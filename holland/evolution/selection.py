import math
import numpy as np
from ..utils import select_from


def select_breeding_pool(fitness_results, top=0, mid=0, bottom=0, random=0):
    """
    Selects a pool of genomes from a population from which to draw parents for breeding the next generation

    :param fitness_results: a sorted list of tuples containing a fitness score in the first position and a genome in the second (returned by :func:`~holland.evolution.evaluate_fitness`)
    :type fitness_results: list

    :param top: number of elements to select from the top of the ``fitness_results``
    :type top: int

    :param mid: number of elements to select from the middle of the ``fitness_results``
    :type mid: int

    :param bottom: number of elements to select from the bottom of the ``fitness_results``
    :type bottom: int

    :param random: number of elements to select randomly from the ``fitness_results``
    :type random: int


    :returns: a list of tuples of the form ``(score, genome)`` (same format as ``fitness_results``)


    :raises ValueError: if ``top + mid + bottom + random > len(fitness_results)``
    :raises ValueError: if any of ``top``, ``mid``, ``bottom``, or ``random`` is negative

    .. note:: For the sake of efficiency, this method expects ``fitness_results`` to be sorted in order to properly select genomes on the basis of fitness. :func:`~holland.evolution.evalute_fitness` returns sorted results.

    Dependencies:
        * :func:`~holland.utils.select_from`
    """
    if top + mid + bottom + random > len(fitness_results):
        raise ValueError(
            "Select Breeding Pool strategy numbers cannot exceed population size"
        )
    if any(value < 0 for value in (top, mid, bottom, random)):
        raise ValueError("Select Bredding Pool strategy numbers cannot be negative")

    selection_pool = select_from(
        fitness_results, top=top, mid=mid, bottom=bottom, random=random
    )

    return selection_pool


def select_parents(fitness_results, weighting_function=lambda x: 1, n_parents=2):
    """
    Selects parents from the given ``fitness_results`` to use for breeding a new genome

    :param fitness_results: a (not necessarily sorted list of tuples containing a fitness score in the first position and a genome in the second (returned by :func:`~holland.evolution.evaluate_fitness`)
    :type fitness_results: list

    :param weighting_function: a function for weighting the probability of selecting a genome based on its fitness, default is uniform probability (i.e. ``lambda x: 1``); see :ref:`selection-strategy`
    :type weighting_function: func

    :param n_parents: the number of genomes to select; see :ref:`selection-strategy`
    :type n_parents: int


    :returns: a list of genomes (of length ``n_parents``)


    :raises ValueError: if ``n_parents < 1``
    """
    if n_parents < 1:
        raise ValueError("Number of parents must be at least 1")

    fitness_scores, genomes = zip(*fitness_results)

    weighted_scores = [weighting_function(fitness) for fitness in fitness_scores]
    min_weighted_score = min(weighted_scores)
    if min_weighted_score < 0:
        max_weighted_score = max(weighted_scores)
        base_shift = abs(min_weighted_score)
        shift = base_shift + (base_shift + max_weighted_score) / 100
        weighted_scores = [ws + shift for ws in weighted_scores]

    weighted_total = sum(weighted_scores)
    selection_probabilities = [
        weighted_score / weighted_total for weighted_score in weighted_scores
    ]

    return np.random.choice(
        genomes, p=selection_probabilities, size=n_parents, replace=False
    )
