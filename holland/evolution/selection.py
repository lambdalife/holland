import math
import numpy as np
from ..utils import select_from


def select_breeding_pool(fitness_results, top=0, mid=0, bottom=0, random=0):
    if top + mid + bottom + random > len(fitness_results):
        raise ValueError(
            "Select Breeding Pool strategy numbers cannot exceed population size"
        )
    if any(value < 0 for value in (top, mid, bottom, random)):
        raise ValueError("Select Bredding Pool strategy numbers cannot be negative")

    sorted_results = sorted(fitness_results, key=lambda x: x[0])
    selection_pool = select_from(
        sorted_results, top=top, mid=mid, bottom=bottom, random=random
    )

    return selection_pool


def select_parents(fitness_results, weighting_function=lambda x: 1, number=2):
    if number < 1:
        raise ValueError("Number of parents must be at least 1")

    fitness_scores, genomes = zip(*fitness_results)

    weighted_scores = [weighting_function(fitness) for fitness in fitness_scores]
    weighted_total = sum(weighted_scores)
    selection_probabilities = [
        weighted_score / weighted_total for weighted_score in weighted_scores
    ]

    return np.random.choice(
        genomes, p=selection_probabilities, size=number, replace=False
    )
