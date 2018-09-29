import math
import numpy as np


def select_breeding_pool(fitness_results, top=0, mid=0, bottom=0, random=0):
    if top + mid + bottom + random > len(fitness_results):
        raise ValueError(
            "Select Pool Narrowing strategy numbers cannot exceed population size"
        )
    if any(value < 0 for value in (top, mid, bottom, random)):
        raise ValueError("Select Pool Narrowing strategy numbers cannot be negative")

    sorted_results = sorted(fitness_results, key=lambda x: x[0])
    selection_pool = []

    if len(sorted_results) % 2 == 0:
        middle_start_index = math.ceil(len(sorted_results) / 2) - math.floor(mid / 2)
    else:
        middle_start_index = math.ceil(len(sorted_results) / 2) - math.ceil(mid / 2)
    selection_pool += sorted_results[-top:]
    selection_pool += sorted_results[middle_start_index : middle_start_index + mid]
    selection_pool += sorted_results[:bottom]

    # use ids because np.random.choice argument must be 1 dimensional
    all_ids = list(range(len(sorted_results)))
    remaining_ids = (
        all_ids[bottom:middle_start_index] + all_ids[middle_start_index + mid : -top]
    )
    random_ids = np.random.choice(remaining_ids, size=random)
    selection_pool += [sorted_results[i] for i in random_ids]

    return selection_pool


def select_parents(fitness_results, weighting_function, number=2):
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
