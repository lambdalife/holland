import random
import numpy as np


def get_uniform_crossover_function():
    def uniform_crossover(parent_genes):
        if type(parent_genes[0]) != list:
            return random.choice(parent_genes)
        return [random.choice(options) for options in zip(*parent_genes)]

    return uniform_crossover


def get_point_crossover_function(num_crossover_points=1):
    def point_crossover(parent_genes):
        crossover_points = sorted(
            np.random.choice(range(1, len(parent_genes[0])), size=num_crossover_points)
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
