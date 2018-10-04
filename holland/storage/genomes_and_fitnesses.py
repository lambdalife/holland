from .utils import record
from ..utils import select_from


def record_genomes_and_fitnesses(generation_num, fitness_results, **storage_options):
    """ Records results of a round of evaluation

        :param generation_num: the generation number of the results
        :type generation_num: int

        :param fitness_results: the results of a round of evaluation (returned by evaluate_fitness)
        :type fitness_results: list

        :param storage_options: options for selecting which results to store and how to store them; see below
        :type storage_options: dict

        :\*\*storage_options:
            * **should_add_generation_suffix** (*bool*) -- determines whether or not to append ``'-generation_{n}'`` to the end of ``file_name``
            * **file_name** (*str*) -- name of the file to write to
            * **format** (*str*) -- file format (options: ``'json'``)
            * **path** (*str*) -- location of the file to write
            * **top** (*int*) -- how many genomes and scores to select from the top of the pack
            * **mid** (*int*) -- how many genomes and scores to select from the middle of the pack
            * **bottom** (*int*) -- how many genomes and scores to select from the bottom of the pack


        :returns: ``None``


        Dependencies:
            * :func:`~holland.storage.format_genomes_and_fitnesses_for_storage`
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
    """ Formats results of a round of evaluation for storage

        :param generation_num: the generation number of the results
        :type generation_num: int

        :param fitness_results: the results of a round of evaluation (returned by evaluate_fitness)
        :type fitness_results: list

        :param storage_options: options for selecting which results to store; see below
        :type storage_options: dict

        :\*\*storage_options:
            * **top** (*int*) -- how many genomes and scores to select from the top of the pack
            * **mid** (*int*) -- how many genomes and scores to select from the middle of the pack
            * **bottom** (*int*) -- how many genomes and scores to select from the bottom of the pack


        :returns: a dictionary of the form ``{"generation": generation_num, "results": selected_results}``


        Dependencies:
            * :func:`~holland.utils.select_from`
    """
    sorted_fitness_results = sorted(fitness_results, key=lambda x: x[0])

    selected_results = select_from(
        sorted_fitness_results,
        top=storage_options.get("top", 0),
        mid=storage_options.get("mid", 0),
        bottom=storage_options.get("bottom", 0),
        random=0,
    )

    return {"generation": generation_num, "results": selected_results}
