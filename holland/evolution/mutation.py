import random

from ..utils import bound_value


def mutate_genome(genome, genome_params):
    """
    Mutates a genome

    :param genome: the genome to mutate
    :type genome: dict

    :param genome_params: a dictionary specifying genome parameters; see :ref:`genome-params`
    :type genome_params: dict


    :returns: a mutated genome


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

    :param gene: the gene to mutate
    :type gene: a valid gene type

    :param gene_params: parameters for a single gene; see :ref:`genome-params`
    :type gene_params: dict

    
    :returns: a mutated gene


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
    Either applies a mutation function to a value of a gene or does not, probabilistically according to the ``mutation_rate``

    :param value: the gene value to mutate
    :type value: a valid, non-list, gene type

    :param mutation_function: a function that mutates the value; see :ref:`mutation-functions`
    :type mutation_function: func

    :param mutation_rate: the probability with which to apply ``mutation_function`` to the value (between 0 and 1)
    :type mutation_rate: float

    :param should_bound: specifies whether or not to bound the mutated value between a maximum and/or minimum
    :type should_bound: bool

    :param minimum: minimum value to bound the mutated value
    :type minimum: int/float

    :param maximum: minimum value to bound the mutated value
    :type maximum: int/float


    :returns: either the mutated value or the original value


    Dependencies:
        * :func:`holland.utils.bound_value`
    """
    if random.random() < mutation_rate:
        mutated_value = mutation_function(value)
        if should_bound:
            mutated_value = bound_value(mutated_value, minimum=minimum, maximum=maximum)
        return mutated_value
    return value
