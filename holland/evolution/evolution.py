from .evaluation import evaluate_fitness
from .breeding import generate_next_generation, generate_random_genomes
from ..storage import record_fitness, record_genomes_and_fitnesses


def evolve(
    fitness_function,
    genome_params,
    selection_strategy,
    population_size=1000,
    random_per_generation=0,
    initial_population=None,
    num_generations=100,
    fitness_storage_options={},
    genome_storage_options={},
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

    fitness_history = []
    for generation_num in range(num_generations):
        try:
            fitness_results = evaluate_fitness(population, fitness_function)

            if fitness_storage_options.get("should_record_fitness", False):
                fitness_scores = [score for score, genome in fitness_results]
                fitness_statistics = record_fitness(
                    generation_num, fitness_scores, **fitness_storage_options
                )
                if fitness_storage_options.get("format") == "memory":
                    fitness_history.append(fitness_statistics)

            is_genome_recording_on = genome_storage_options.get(
                "should_record_genomes", False
            )
            is_valid_generation_num = (
                generation_num
                % genome_storage_options.get("record_every_n_generations", 1)
                == 0
            )
            if is_genome_recording_on and is_valid_generation_num:
                record_genomes_and_fitnesses(
                    generation_num, fitness_results, **genome_storage_options
                )

            if generation_num < num_generations - 1:
                population = generate_next_generation(
                    fitness_results,
                    genome_params,
                    selection_strategy,
                    population_size=population_size,
                    random_per_generation=random_per_generation,
                )
        except:
            if genome_storage_options.get("should_record_on_interrupt", False):
                record_genomes_and_fitnesses(
                    generation_num, fitness_results, **genome_storage_options
                )
            raise

    if (
        fitness_storage_options.get("should_record_fitness", False)
        and fitness_storage_options.get("format") == "memory"
    ):
        return fitness_results, fitness_history
    return fitness_results
