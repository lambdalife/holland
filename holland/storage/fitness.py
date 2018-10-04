import statistics

from .utils import record


def record_fitness(generation_num, fitness_scores, **storage_options):
    fitness_statistics = format_fitness_statistics(generation_num, fitness_scores)

    record(fitness_statistics, **storage_options)

    return fitness_statistics


def format_fitness_statistics(generation_num, fitness_scores):
    return {
        "generation": generation_num,
        "max": max(fitness_scores),
        "min": min(fitness_scores),
        "median": statistics.median(fitness_scores),
        "mean": statistics.mean(fitness_scores),
        "stdev": statistics.stdev(fitness_scores),
    }
