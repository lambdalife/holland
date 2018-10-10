from .fitness import record_fitness
from .genomes_and_fitnesses import record_genomes_and_fitnesses


class StorageManager:
    """
    Handles recording fitness statistics and genomes.

    :param fitness_storage_options: options for storing fitness statistics; see :ref:`fitness-storage-options`
    :type fitness_storage_options: dict

    :param genome_storage_options: options for storing genomes and their fitness scores; see :ref:`genome-storage-options`
    :type genome_storage_options: dict
    """

    def __init__(self, fitness_storage_options={}, genome_storage_options={}):
        self.fitness_storage_options = fitness_storage_options
        self.should_record_fitness = fitness_storage_options.get(
            "should_record_fitness"
        )
        self.fitness_format = fitness_storage_options.get("format")
        self.fitness_history = []

        self.genome_storage_options = genome_storage_options
        self.should_record_genomes = genome_storage_options.get("should_record_genomes")
        self.genome_recording_frequency = genome_storage_options.get(
            "record_every_n_generations", 1
        )
        self.should_record_genomes_on_interrupt = genome_storage_options.get(
            "should_record_on_interrupt"
        )

    def update_storage(self, generation_num, fitness_results):
        """
        Updates storage of fitness scores and genomes (with fitness scores) when called; Decisions for whether to record or not are handled by dependencies

        :param generation_num: the generation number of the population that generated the ``fitness_results``
        :type generation_num: int

        :param fitness_results: the results of a round of evaluation (returned by :func:`~holland.evolution.evaluate_fitness`)
        :type fitness_results: list


        :returns: ``None``


        Dependencies:
            * :func:`~holland.storage.StorageManager.update_fitness_storage`
            * :func:`~holland.storage.StorageManager.update_genome_storage`
        """
        self.update_fitness_storage(generation_num, fitness_results)
        self.update_genome_storage(generation_num, fitness_results)

    def react_to_interruption(self, generation_num, fitness_results):
        """
        Updates storage of genomes (with fitness scores) in the event of an interruption during execution if ``genome_storage_options["should_record_on_interrupt"]`` is set to ``True``

        :param generation_num: the generation number of the population that generated the ``fitness_results``
        :type generation_num: int

        :param fitness_results: the results of a round of evaluation (returned by :func:`~holland.evolution.evaluate_fitness`)
        :type fitness_results: list


        :returns: ``None``


        Dependencies:
            * :func:`~holland.storage.record_genomes_and_fitnesses`
        """
        if self.should_record_genomes_on_interrupt:
            record_genomes_and_fitnesses(
                generation_num, fitness_results, **self.genome_storage_options
            )

    def update_fitness_storage(self, generation_num, fitness_results):
        """
        Updates storage of fitness scores if ``fitness_storage_options["should_record_fitness"]`` is set to ``True``

        :param generation_num: the generation number of the population that generated the ``fitness_results``
        :type generation_num: int

        :param fitness_results: the results of a round of evaluation (returned by :func:`~holland.evolution.evaluate_fitness`)
        :type fitness_results: list

        :returns: ``None``


        Dependencies:
            * :func:`~holland.storage.record_fitness`
        """
        if self.should_record_fitness:
            fitness_scores = [fitness for fitness, genome in fitness_results]
            fitness_stats = record_fitness(
                generation_num, fitness_scores, **self.fitness_storage_options
            )
            if self.fitness_format == "memory":
                self.fitness_history.append(fitness_stats)

    def update_genome_storage(self, generation_num, fitness_results):
        """
        Updates storage of genomes (with fitness scores) if ``genome_storage_options["should_record_genomes"]`` is set to ``True`` and the ``generation_num`` matches the recording frequency

        :param generation_num: the generation number of the population that generated the ``fitness_results``
        :type generation_num: int

        :param fitness_results: the results of a round of evaluation (returned by :func:`~holland.evolution.evaluate_fitness`)
        :type fitness_results: list


        :returns: ``None``


        Dependencies:
            * :func:`~holland.storage.StorageManager.should_record_genomes_now`
            * :func:`~holland.storage.record_genomes_and_fitnesses`
        """
        if self.should_record_genomes_now(generation_num):
            record_genomes_and_fitnesses(
                generation_num, fitness_results, **self.genome_storage_options
            )

    def should_record_genomes_now(self, current_generation_num):
        """
        Returns a boolean telling whether genomes should be recorded for the ``current_generation_num`` or not; Returns ``True`` if ``genome_storage_options["should_record_genomes"]`` is set to ``True`` and the ``generation_num`` matches the recording frequency, otherwise ``False``

        :param generation_num: the generation number of the population that generated the ``fitness_scores``
        :type generation_num: int


        :returns: a boolean telling whether or not genomes should be recorded
        """
        return (
            self.should_record_genomes
            and current_generation_num % self.genome_recording_frequency == 0
        )
