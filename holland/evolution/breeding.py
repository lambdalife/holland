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
    """
    testing generate next generation

    :param fitness_results: a list of fitness scores from the previous generation
    :type fitness_results: list

    :param genome_params: a dictionary specifying genome parameters
    :type genome_params: dict
    
    :param selection_strategy: a dictionary specifying selection parameters
    :type selection_strategy: dict
    
    :param random_per_generation: the number of random genomes to introduce per generation
    :type random_per_generation: int
    
    :param population_size: the size of the population
    :type population_size: int or None


    :returns: a list of genomes


    Dependencies:
        * :func:`~holland.evolution.breed_next_generation`
        * :func:`~holland.evolution.generate_random_genomes`
    """
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
                genome[gene_name] = [
                    bound_value(
                        gene_params["initial_distribution"](),
                        minimum=gene_params.get("min"),
                        maximum=gene_params.get("max"),
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
