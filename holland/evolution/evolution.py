from .evaluation import evaluate_fitness
from .breeding import generate_next_generation, generate_random_genomes


def evolve(
    fitness_function,
    genome_params,
    selection_strategy,
    population_size=1000,
    random_per_generation=0,
    initial_population=None,
    num_generations=100,
):
    """ The heart of Holland.

        :param fitness_function: the fitness function used to evaluate individuals
        :type fitness_function: function
        
        :param genome_params: a dictionary specifying genome parameters
        :type genome_params: dict

        :param selection_strategy: a dictionary specifying selection parameters
        :type selection_strategy: dict

        :param population_size: the size of the population
        :type population_size: int

        :param random_per_generation: the number of random genomes to introduce per generation
        :type random_per_generation: int

        :param initial_population: an initial population
        :type initial_population: list

        :param num_generations: the number of generations to evolve the population       
        :type num_generations: int    

        :returns: a list of fitness scores


        :raises ValueError: if random_per_generation < 0
        :raises ValueError: if population_size < 1
        :raises ValueError: if num_generation < 1


        .. todo:: If an initial population is given but does not match the given genome parameters, some kind of error should be raised
        .. todo:: If an initial population is given and some genomes are missing parameters, a warning is given unless a flag is set to fill those values randomly

        Dependencies:
            * :func:`~holland.evolution.generate_next_generation`
            * :func:`~holland.evolution.evaluate_fitness`

    """
    if random_per_generation < 0:
        raise ValueError("Number of random genomes per generation cannot be negative")
    if population_size < 1:
        raise ValueError("Population size must be at least 1")
    if num_generations < 1:
        raise ValueError("Number of generations must be at least 1")

    population = initial_population
    if population is None:
        population = generate_random_genomes(genome_params, population_size)

    fitness_results = evaluate_fitness(population, fitness_function)

    for gen_num in range(1, num_generations):
        population = generate_next_generation(
            fitness_results,
            genome_params,
            selection_strategy,
            population_size=population_size,
            random_per_generation=random_per_generation,
        )

        fitness_results = evaluate_fitness(population, fitness_function)

    return fitness_results
