from .utils import record
from ..utils import select_from


def record_genomes_and_fitnesses(generation_num, fitness_results, **storage_options):
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
    sorted_fitness_results = sorted(fitness_results, key=lambda x: x[0])

    selected_results = select_from(
        sorted_fitness_results,
        top=storage_options.get("top", 0),
        mid=storage_options.get("mid", 0),
        bottom=storage_options.get("bottom", 0),
        random=0,
    )

    return {"generation": generation_num, "results": selected_results}
