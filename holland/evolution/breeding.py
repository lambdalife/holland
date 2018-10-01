import numpy as np

from .selection import select_breeding_pool, select_parents
from .crossover import cross
from .mutation import mutate_genome
from ..utils import bound_value


def generate_next_generation(
    fitness_results,
    genome_params,
    selection_strategy,
    random_per_generation=0,
    population_size=None,
):
    if population_size is None:
        population_size = len(fitness_results)

    bred_per_generation = population_size - random_per_generation

    return [
        *breed_next_generation(
            fitness_results, genome_params, selection_strategy, bred_per_generation
        ),
        *generate_random_genomes(genome_params, random_per_generation),
    ]


def breed_next_generation(fitness_results, genome_params, selection_strategy, number):
    if number < 0:
        raise ValueError("Number of bred genomes per generation cannot be negative")

    breeding_pool = select_breeding_pool(
        fitness_results, **selection_strategy.get("pool")
    )

    next_generation = []

    for _ in range(number):
        parents = select_parents(breeding_pool, **selection_strategy.get("parents"))
        offspring = cross(parents, genome_params)
        mutated_offspring = mutate_genome(offspring, genome_params)
        next_generation.append(mutated_offspring)

    return next_generation


def generate_random_genomes(genome_params, number):
    if number < 0:
        raise ValueError("Number of random genomes per generation cannot be negative")

    genomes = []

    for _ in range(number):
        genome = {}
        for gene_name, gene_params in genome_params.items():
            if gene_params["type"] == "float":
                min_bound = (
                    gene_params.get("min") if "min" in gene_params.keys() else -np.inf
                )
                max_bound = (
                    gene_params.get("max") if "max" in gene_params.keys() else np.inf
                )
                genome[gene_name] = [
                    bound_value(
                        gene_params["initial_distribution"](), min_bound, max_bound
                    )
                    for _ in range(gene_params["size"])
                ]
            else:
                genome[gene_name] = [
                    gene_params["initial_distribution"]()
                    for _ in range(gene_params["size"])
                ]
        genomes.append(genome)

    return genomes
