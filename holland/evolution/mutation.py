import random

from ..utils import bound_value


def mutate_genome(genome, genome_params):
    """
    mutates a given genome

    :param genome:
    :type genome:

    :parame genome_params:
    :type genome_params:


    :returns: a mutated genome


    .. todo:: fill in param information
    .. todo:: write an example


    Dependencies:
        * :func:`holland.evolution.mutate_gene`
    """
    return {
        gene_name: mutate_gene(genome[gene_name], genome_params[gene_name])
        for gene_name in genome.keys()
    }


def mutate_gene(gene, gene_params):
    """
    Mutates a single gene

    :param gene: The gene to mutate
    :type gene: one of gene types

    :param gene_params:
    :type gene_params: dict

    
    :returns: a mutated gene

    .. todo:: fill in param information
    .. todo:: add a link to the avilable gene types
    .. todo:: write an example


    Dependencies:
        * :func:`holland.evolution.probabilistically_mutate_value`
    """
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

    """ 
    Randomly changes a given value based on a mutation function

    :param value:
    :type value:

    :param mutation_function:
    :type mutation_function:

    :param mutation_rate:
    :type mutation_rate:

    :param should_bound:
    :type should_bound:

    :param minimum:
    :type minimum:

    :param maximum:
    :type maximum:


    :returns: the altered value


    .. todo:: write an example


    Dependencies:
        * :ref:`mutation-functions`
        * :func:`holland.utils.bound_value`
    """
    if random.random() < mutation_rate:
        mutated_value = mutation_function(value)
        if should_bound:
            mutated_value = bound_value(mutated_value, minimum=minimum, maximum=maximum)
        return mutated_value
    return value
