import math

from .evaluation import Evaluator
from .breeding import PopulationGenerator
from ..storage import StorageManager


class Evolver:
    """
    Handles evolution for a population

    :param fitness_function: the fitness function used to evaluate individuals; see :ref:`fitness-function`
    :type fitness_function: function
    
    :param genome_params: a dictionary specifying genome parameters; see :ref:`genome-params`
    :type genome_params: dict

    :param selection_strategy: a dictionary specifying selection parameters; see :ref:`selection-strategy`
    :type selection_strategy: dict

    :param should_maximize_fitness: whether fitness should be maximized or minimized
    :type should_maximize_fitness: bool
    """

    def __init__(
        self,
        fitness_function,
        genome_params,
        selection_strategy,
        should_maximize_fitness=True,
    ):
        self.fitness_function = fitness_function
        self.genome_params = genome_params
        self.selection_strategy = selection_strategy
        self.should_maximize_fitness = should_maximize_fitness

    def evolve(
        self,
        generation_params={},
        initial_population=None,
        stop_conditions={"n_generations": 100, "target_fitness": math.inf},
        storage_options={},
    ):
        """
        The heart of Holland.

        :param generation_params: a dictionary specifying how to create each generation; see :ref:`generation-params`
        :type generation_params: dict

        :param initial_population: an initial population
        :type initial_population: list

        :param stop_conditions: conditions for stopping execution; will stop if *any* of the conditions is met; see Stop Conditions below
        :type stop_conditions: dict
    
        :param storage_options: configuration options for storing fitness and genomes (should contain keys ``"fitness"`` and ``"genomes"``); see :ref:`fitness-storage-options` and :ref:`genome-storage-options`
        :type storage_options: dict

        :Stop Conditions:
            * **n_generations** (*int*) -- the number of generations to run evolution over
            * **target_fitness** (*int*) -- the target fitness score, will stop once the fittest individual reaches this score


        :returns:
            * a list of fitness scores and genomes ``[(fitness, genome), ...]`` (fitness results); or
            * a tuple of fitness results (previous bullet) and list of historical fitness statistics ``(fitness_results, fitness_history)``,  if ``storage_options["fitness"]`` has ``'should_record_fitness': True`` and ``'format': 'memory'``


        :raises ValueError: if ``generation_params["n_random"] < 0`` or ``generation_params["n_elite"] < 0``
        :raises ValueError: if ``population_size < 1``
        :raises ValueError: if ``n_generations < 1``


        .. todo:: If an initial population is given but does not match the given genome parameters, some kind of error should be raised
        .. todo:: If an initial population is given and some genomes are missing parameters, a warning is given unless a flag is set to fill those values randomly

        Dependencies:
            * :func:`~holland.evolution.PopulationGenerator.generate_random_genomes`
            * :func:`~holland.evolution.Evaluator.evaluate_fitness`
            * :func:`~holland.evolution.PopulationGenerator.generate_next_generation`
            * :func:`~holland.storage.StorageManager.update_storage`
            * :func:`~holland.storage.StorageManager.react_to_interruption`


        Example:
            .. literalinclude:: examples/basic_example.py
                :linenos:
                :emphasize-lines: 23-26
        """
        n_random_per_generation = generation_params.get("n_random", 0)
        n_elite_per_generation = generation_params.get("n_elite", 0)
        population_size = generation_params.get("population_size", 1000)
        n_generations = stop_conditions.get("n_generations", math.inf)
        target_fitness = stop_conditions.get("target_fitness", math.inf)
        should_stop = (
            lambda gen_num, max_fit: gen_num == n_generations - 1
            or max_fit == target_fitness
        )

        if n_random_per_generation < 0 or n_elite_per_generation < 0:
            raise ValueError(
                "Number of random and elite genomes per generation cannot be negative"
            )
        if population_size < 1:
            raise ValueError("Population size must be at least 1")
        if n_generations < 1:
            raise ValueError("Number of generations must be at least 1")

        evaluator = Evaluator(
            self.fitness_function, ascending=self.should_maximize_fitness
        )
        storage_manager = StorageManager(
            fitness_storage_options=storage_options.get("fitness", {}),
            genome_storage_options=storage_options.get("genomes", {}),
        )
        population_generator = PopulationGenerator(
            self.genome_params,
            self.selection_strategy,
            generation_params=generation_params,
        )

        population = initial_population
        if population is None:
            population = population_generator.generate_random_genomes(population_size)

        generation_num = 0
        while True:
            try:
                fitness_results = evaluator.evaluate_fitness(population)

                storage_manager.update_storage(generation_num, fitness_results)

                max_fitness = fitness_results[-1][0]
                if should_stop(generation_num, max_fitness):
                    break

                population = population_generator.generate_next_generation(
                    fitness_results
                )

                generation_num += 1
            except:
                storage_manager.react_to_interruption(generation_num, fitness_results)
                raise

        if (
            storage_options.get("fitness", {}).get("should_record_fitness", False)
            and storage_options.get("fitness", {}).get("format") == "memory"
        ):
            return fitness_results, storage_manager.fitness_history
        return fitness_results
