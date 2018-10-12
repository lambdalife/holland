import math
import numpy as np
from ..utils import select_from


class Selector:
    """
    Handles selection of genomes for breeding

    :param selection_strategy: parameters for selecting a breeding pool and sets of parents; see :ref:`selection-strategy`

    :raises ValueError: if any of ``top``, ``mid``, ``bottom``, or ``random`` is negative
    :raises ValueError: if ``n_parents < 1``
    """

    def __init__(self, selection_strategy={}):
        pool_strategy = selection_strategy.get("pool", {})
        self.top = pool_strategy.get("top", 0)
        self.mid = pool_strategy.get("mid", 0)
        self.bottom = pool_strategy.get("bottom", 0)
        self.random = pool_strategy.get("random", 0)

        if any(value < 0 for value in (self.top, self.mid, self.bottom, self.random)):
            raise ValueError("Select Bredding Pool strategy numbers cannot be negative")

        parents_strategy = selection_strategy.get("parents", {})
        self.weighting_function = parents_strategy.get("weighting_function", lambda x: 1)
        self.n_parents = parents_strategy.get("n_parents", 2)

        if self.n_parents < 1:
            raise ValueError("Number of parents must be at least 1")

    def select_breeding_pool(self, fitness_results):
        """
        Selects a pool of genomes from a population from which to draw parents for breeding the next generation

        :param fitness_results: a sorted list of tuples containing a fitness score in the first position and a genome in the second (returned by :func:`~holland.evolution.Evaluator.evaluate_fitness`)
        :type fitness_results: list


        :returns: a list of tuples of the form ``(score, genome)`` (same format as ``fitness_results``)


        :raises ValueError: if ``len(fitness_results) < self.top + self.mid + self.bottom + self.random``

        .. note:: For the sake of efficiency, this method expects ``fitness_results`` to be sorted in order to properly select genomes on the basis of fitness. :func:`~holland.evolution.Evaluator.evaluate_fitness` returns sorted results.

        Dependencies:
            * :func:`~holland.utils.utils.select_from`
        """
        if self.top + self.mid + self.bottom + self.random > len(fitness_results):
            raise ValueError("Select Breeding Pool strategy numbers cannot exceed population size")

        selection_pool = select_from(
            fitness_results, top=self.top, mid=self.mid, bottom=self.bottom, random=self.random
        )

        return selection_pool

    def select_parents(self, fitness_results):
        """
        Selects parents from the given ``fitness_results`` to use for breeding a new genome

        :param fitness_results: a (not necessarily sorted list of tuples containing a fitness score in the first position and a genome in the second (returned by :func:`~holland.evolution.Evaluator.evaluate_fitness`)
        :type fitness_results: list


        :returns: a list of genomes (of length ``self.n_parents``)
        """
        fitness_scores, genomes = zip(*fitness_results)

        weighted_scores = [self.weighting_function(fitness) for fitness in fitness_scores]
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
            genomes, p=selection_probabilities, size=self.n_parents, replace=False
        )
