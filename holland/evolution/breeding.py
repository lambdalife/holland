import numpy as np

from .selection import select_breeding_pool, select_parents
from .crossover import cross_genomes
from .mutation import mutate_genome
from ..utils import bound_value, is_numeric_type, is_list_type


def generate_next_generation(
    fitness_results,
    genome_params,
    selection_strategy,
    n_random=0,
    n_elite=0,
    population_size=None,
):
    """
    Generates the next generation

    :param fitness_results: a sorted list of tuples containing a fitness score in the first position and a genome in the second (returned by :func:`~holland.evolution.evaluate_fitness`)
    :type fitness_results: list

    :param genome_params: a dictionary specifying genome parameters; see :ref:`genome-params`
    :type genome_params: dict
    
    :param selection_strategy: a dictionary specifying selection parameters; see :ref:`selection-strategy`
    :type selection_strategy: dict
    
    :param n_random: the number of random genomes to introduce
    :type n_random: int

    :param n_elite: the number of genomes from the current generation to preserve for the next generation unchanged (starting with the most fit genome)
    :type n_elite: int
    
    :param population_size: the size of the population (defaults to length of ``fitness_results``)
    :type population_size: int or None


    :returns: a list of genomes

    
    :raises ValueError: if ``n_random < 0`` or ``n_elite < 0``
    :raises ValueError: if ``n_random + n_elite > population_size``

    
    .. note:: For the sake of efficiency, this method expects ``fitness_results`` to be sorted in order to properly select genomes on the basis of fitness. :func:`~holland.evolution.evalute_fitness` returns sorted results.

    .. todo:: Write an example for usage


    Dependencies:
        * :func:`~holland.evolution.breed_next_generation`
        * :func:`~holland.evolution.generate_random_genomes`
    """
    if n_random < 0 or n_elite < 0:
        raise ValueError("Number of random or elite individuals cannot be negative")

    if population_size is None:
        population_size = len(fitness_results)

    if n_random + n_elite > population_size:
        raise ValueError(
            "Number of random and elite individuals must be less than or equal to population size"
        )

    bred_per_generation = population_size - n_random - n_elite

    if n_elite > 0:
        elite_genomes = [genome for fitness, genome in fitness_results[-n_elite:]]
    else:
        elite_genomes = []

    bred_genomes = breed_next_generation(
        fitness_results, genome_params, selection_strategy, bred_per_generation
    )
    random_genomes = generate_random_genomes(genome_params, n_random)

    return elite_genomes + bred_genomes + random_genomes


def breed_next_generation(
    fitness_results, genome_params, selection_strategy, n_genomes
):
    """
    Generates a given number of genomes by breeding, through crossover and mutation, existing genomes

    :param fitness_results: a sorted list of tuples containing a fitness score in the first position and a genome in the second (returned by :func:`~holland.evolution.evaluate_fitness`)
    :type fitness_results: list

    :param genome_params: a dictionary specifying genome parameters; see :ref:`genome-params`
    :type genome_params: dict

    :param selection_strategy: a dictionary specifying selection parameters; see :ref:`selection-strategy`
    :type selection_strategy: dict

    :param n_genomes: the number of genomes to produce
    :type n_genomes: int


    :returns: a list of bred genomes


    :raises ValueError: if ``n_genomes < 0``

    
    .. note:: For the sake of efficiency, this method expects ``fitness_results`` to be sorted in order to properly select genomes on the basis of fitness. :func:`~holland.evolution.evalute_fitness` returns sorted results.

    .. todo:: Write an example for usage


    Dependencies:
        * :func:`~holland.evolution.select_breeding_pool`
        * :func:`~holland.evolution.select_parents`
        * :func:`~holland.evolution.cross_genomes`
        * :func:`~holland.evolution.mutate_genome`
    """
    if n_genomes < 0:
        raise ValueError("Number of bred genomes per generation cannot be negative")

    breeding_pool = select_breeding_pool(
        fitness_results, **selection_strategy.get("pool")
    )

    next_generation = []

    for _ in range(n_genomes):
        parents = select_parents(breeding_pool, **selection_strategy.get("parents"))
        offspring = cross_genomes(parents, genome_params)
        mutated_offspring = mutate_genome(offspring, genome_params)
        next_generation.append(mutated_offspring)

    return next_generation


def generate_random_genomes(genome_params, n_genomes):
    """
    Generates a given number of genomes based on genome parameters

    :param genome_params: a dictionary specifying genome parameters; see :ref:`genome-params`
    :type genome_params: dict

    :param n_genomes: the number of genomes to produce
    :type n_genomes: int


    :returns: a list of randomly generated genomes


    :raises ValueError: if ``n_genomes < 0``

    .. todo:: Write an example for usage

    Dependencies:
        * :func:`holland.utils.bound_value`
    """
    if n_genomes < 0:
        raise ValueError("Number of random genomes per generation cannot be negative")

    genomes = []

    for _ in range(n_genomes):
        genome = {}
        for gene_name, gene_params in genome_params.items():
            initial_distribution = gene_params["initial_distribution"]
            if is_list_type(gene_params):
                if is_numeric_type(gene_params):
                    genome[gene_name] = [
                        bound_value(
                            initial_distribution(),
                            minimum=gene_params.get("min"),
                            maximum=gene_params.get("max"),
                            to_int=gene_params.get("type") == "[int]",
                        )
                        for _ in range(gene_params["size"])
                    ]
                else:
                    genome[gene_name] = [
                        initial_distribution() for _ in range(gene_params["size"])
                    ]
            else:
                if is_numeric_type(gene_params):
                    genome[gene_name] = bound_value(
                        initial_distribution(),
                        minimum=gene_params.get("min"),
                        maximum=gene_params.get("max"),
                        to_int=gene_params.get("type") == "int",
                    )
                else:
                    genome[gene_name] = initial_distribution()
        genomes.append(genome)

    return genomes
