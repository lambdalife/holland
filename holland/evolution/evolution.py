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
