from .utils import record
from ..utils import select_from


def record_genomes_and_fitnesses(generation_num, fitness_results, **storage_options):
    """
    Records results of a round of evaluation

    :param generation_num: the generation number of the population that generated the fitness_scores
    :type generation_num: int

    :param fitness_results: the results of a round of evaluation (returned by :func:`~holland.evolution.Evaluator.evaluate_fitness`)
    :type fitness_results: list

    :param storage_options: options for selecting which results to store and how to store them, specifically ``should_add_generation_suffix``, ``format``, ``file_name``, ``path``, ``top``, ``mid``, ``bottom`` are relevant; see :ref:`genome-storage-options`
    :type storage_options: dict


    :returns: ``None``


    Dependencies:
        * :func:`~holland.storage.genomes_and_fitnesses.format_genomes_and_fitnesses_for_storage`
    """
    formatted_data = format_genomes_and_fitnesses_for_storage(
        generation_num, fitness_results, **storage_options
    )

    if storage_options.get("should_add_generation_suffix", False):
        file_name = storage_options["file_name"]
        splitted_file_name = file_name.split(".")
        splitted_file_name[0] += "-generation_{}".format(generation_num)
        updated_file_name = ".".join(splitted_file_name)
        storage_options["file_name"] = updated_file_name

    record(formatted_data, **storage_options)


def format_genomes_and_fitnesses_for_storage(
    generation_num, fitness_results, **storage_options
):
    """
    Formats results of a round of evaluation for storage

    :param generation_num: the generation number of the results
    :type generation_num: int

    :param fitness_results: the sorted results of a round of evaluation (returned by evaluate_fitness)
    :type fitness_results: list

    :param storage_options: options for selecting which results to store, specifically ``top``, ``mid``, ``bottom`` are relevant; see :ref:`genome-storage-options`
    :type storage_options: dict


    :returns: a dictionary of the form ``{"generation": generation_num, "results": selected_results}``


    .. note:: For the sake of efficiency, this method expects ``fitness_results`` to be sorted in order to properly select genomes on the basis of fitness. :func:`~holland.evolution.Evaluator.evaluate_fitness` returns sorted results.

    Dependencies:
        * :func:`~holland.utils.utils.select_from`
    """
    selected_results = select_from(
        fitness_results,
        top=storage_options.get("top", 0),
        mid=storage_options.get("mid", 0),
        bottom=storage_options.get("bottom", 0),
        random=0,
    )

    return {"generation": generation_num, "results": selected_results}
