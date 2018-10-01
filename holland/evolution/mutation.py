import random

from ..utils import bound_value


def mutate_genome(genome, genome_params):
    return {
        gene_name: mutate_gene(genome[gene_name], genome_params[gene_name])
        for gene_name in genome.keys()
    }


def mutate_gene(gene, gene_params):
    mutation_function = gene_params["mutation_function"]
    mutation_rate = gene_params["mutation_rate"]
    should_bound = gene_params.get("type") == "float"
    minimum = gene_params.get("min")
    maximum = gene_params.get("max")

    return [
        probabilistically_mutate_value(
            value,
            mutation_function,
            mutation_rate=mutation_rate,
            should_bound=should_bound,
            minimum=minimum,
            maximum=maximum,
        )
        for value in gene
    ]


def probabilistically_mutate_value(
    value,
    mutation_function,
    mutation_rate=0.001,
    should_bound=False,
    minimum=None,
    maximum=None,
):
    if random.random() < mutation_rate:
        mutated_value = mutation_function(value)
        if should_bound:
            mutated_value = bound_value(mutated_value, minimum=minimum, maximum=maximum)
        return mutated_value
    return value
