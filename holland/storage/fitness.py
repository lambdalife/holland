import statistics

from .utils import record


def record_fitness(generation_num, fitness_scores, **storage_options):
    """ Records fitness statistics for a generation to a file and returns fitness statistics

        :param generation_num: the generation number of the population that generated the fitness_scores
        :type generation_num: int

        :param fitness_scores: the fitness scores of the generation
        :type fitness_scores: list

        :param storage_options: options for storing statistics, specifically ``file_name``, ``format``, and ``path`` are relevant; see :ref:`fitness-storage-options`
        :type storage_options: dict


        :returns: a dictionary of statistics for the fitness scores
        

        Dependencies:
            * :func:`~holland.storage.format_fitness_statistics`
    """
    fitness_statistics = format_fitness_statistics(generation_num, fitness_scores)

    record(fitness_statistics, **storage_options)

    return fitness_statistics


def format_fitness_statistics(generation_num, fitness_scores):
    """ Generate statistics on fitness scores for a generation

        :param generation_num: the generation number of the population that generated the fitness_scores
        :type generation_num: int

        :param fitness_scores: the fitness scores of the generation
        :type fitness_scores: list


        :returns: a dictionary of statistics for the fitness scores
    """
    return {
        "generation": generation_num,
        "max": max(fitness_scores),
        "min": min(fitness_scores),
        "median": statistics.median(fitness_scores),
        "mean": statistics.mean(fitness_scores),
        "stdev": statistics.stdev(fitness_scores),
    }
