import random

from ..utils import bound_value, is_numeric_type, is_list_type


class Mutator:
    """
    Handles genetic mutation

    :param genome_params: a dictionary specifying genome parameters; see :ref:`genome-params`
    :type genome_params: dict
    """

    def __init__(self, genome_params):
        self.genome_params = genome_params

    def mutate_genome(self, genome):
        """
        Mutates a genome

        :param genome: the genome to mutate
        :type genome: dict


        :returns: a mutated genome


        Dependencies:
            * :func:`holland.evolution.Mutator.mutate_gene`
        """
        return {
            gene_name: self.mutate_gene(
                genome[gene_name], self.genome_params[gene_name]
            )
            for gene_name in self.genome_params.keys()
        }

    def mutate_gene(self, gene, gene_params):
        """
        Mutates a single gene

        :param gene: the gene to mutate
        :type gene: a valid gene type

        :param gene_params: parameters for a single gene; see :ref:`genome-params`
        :type gene_params: dict

        
        :returns: a mutated gene


        Dependencies:
            * :func:`holland.evolution.Mutator.probabilistically_mutate_value`
        """
        if is_list_type(gene_params):
            return [
                self.probabilistically_mutate_value(value, gene_params)
                for value in gene
            ]

        return self.probabilistically_mutate_value(gene, gene_params)

    def probabilistically_mutate_value(self, value, gene_params):

        """
        Either applies a mutation function to a value of a gene or does not, probabilistically according to the ``mutation_rate``

        :param value: the gene value to mutate
        :type value: a valid, non-list, gene type

        :param gene_params: parameters for a single gene; see :ref:`genome-params`
        :type gene_params: dict


        :returns: either the mutated value or the original value


        Dependencies:
            * :func:`holland.utils.bound_value`
        """
        mutation_function = gene_params["mutation_function"]
        mutation_rate = gene_params["mutation_rate"]
        should_bound = is_numeric_type(gene_params)
        to_int = gene_params.get("type") in ["int", "[int]"]
        minimum = gene_params.get("min")
        maximum = gene_params.get("max")

        if random.random() < mutation_rate:
            mutated_value = mutation_function(value)
            if should_bound:
                mutated_value = bound_value(
                    mutated_value, minimum=minimum, maximum=maximum, to_int=to_int
                )
            return mutated_value
        return value
