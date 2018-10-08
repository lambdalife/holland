from .evaluation import evaluate_fitness
from .breeding import generate_next_generation, generate_random_genomes
from ..storage import record_fitness, record_genomes_and_fitnesses


def evolve(
    fitness_function,
    genome_params,
    selection_strategy,
    should_maximize_fitness=True,
    population_size=1000,
    n_random_per_generation=0,
    n_elite_per_generation=0,
    initial_population=None,
    n_generations=100,
    fitness_storage_options={},
    genome_storage_options={},
):
    """
    The heart of Holland.

    :param fitness_function: the fitness function used to evaluate individuals; see :ref:`fitness-function`
    :type fitness_function: function
    
    :param genome_params: a dictionary specifying genome parameters; see :ref:`genome-params`
    :type genome_params: dict

    :param selection_strategy: a dictionary specifying selection parameters; see :ref:`selection-strategy`
    :type selection_strategy: dict

    :param should_maximize_fitness: whether fitness should be maximized or minimized
    :type should_maximize_fitness: bool

    :param population_size: the size of the population
    :type population_size: int

    :param n_random_per_generation: the number of random genomes to introduce per generation
    :type n_random_per_generation: int

    :param n_elite_per_generation: the number of genomes from the current generation to preserve for the next generation unchanged (starting with the most fit genome)
    :type n_elite_per_generation: int

    :param initial_population: an initial population
    :type initial_population: list

    :param n_generations: the number of generations to run evolution over
    :type n_generations: int

    :param fitness_storage_options: configuration options for storing fitness score statistics over time; see :ref:`fitness-storage-options`
    :type fitness_storage_options: dict

    :param genome_storage_options: configuration options for storing genomes; see :ref:`genome-storage-options`
    :type genome_storage_options: dict


    :returns:
        * a list of fitness scores and genomes ``[(fitness, genome), ...]`` (fitness results); or
        * a tuple of fitness results (previous bullet) and list of historical fitness statistics ``(fitness_results, fitness_history)``,  if ``fitness_storage_options`` has ``'should_record_fitness': True`` and ``'format': 'memory'``


    :raises ValueError: if ``n_random_per_generation < 0`` or ``n_elite_per_generation < 0``
    :raises ValueError: if ``population_size < 1``
    :raises ValueError: if ``num_generation < 1``


    .. todo:: If an initial population is given but does not match the given genome parameters, some kind of error should be raised
    .. todo:: If an initial population is given and some genomes are missing parameters, a warning is given unless a flag is set to fill those values randomly

    Dependencies:
        * :func:`~holland.evolution.evaluate_fitness`
        * :func:`~holland.evolution.generate_next_generation`
        * :func:`~holland.storage.record_fitness`
        * :func:`~holland.storage.record_genomes_and_fitnesses`



    Example:
        .. literalinclude:: examples/basic_example.py
            :linenos:
            :emphasize-lines: 23-26
    """
    if n_random_per_generation < 0 or n_elite_per_generation < 0:
        raise ValueError(
            "Number of random and elite genomes per generation cannot be negative"
        )
    if population_size < 1:
        raise ValueError("Population size must be at least 1")
    if n_generations < 1:
        raise ValueError("Number of generations must be at least 1")

    population = initial_population
    if population is None:
        population = generate_random_genomes(genome_params, population_size)

    fitness_history = []
    for generation_num in range(n_generations):
        try:
            fitness_results = evaluate_fitness(
                population, fitness_function, ascending=should_maximize_fitness
            )

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

            if generation_num < n_generations - 1:
                population = generate_next_generation(
                    fitness_results,
                    genome_params,
                    selection_strategy,
                    population_size=population_size,
                    n_random=n_random_per_generation,
                    n_elite=n_elite_per_generation,
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
