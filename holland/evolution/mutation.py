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
            * :func:`~holland.evolution.Mutator.mutate_gene`
        """
        return {
            gene_name: self.mutate_gene(genome[gene_name], self.genome_params[gene_name])
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
            * :func:`~holland.evolution.Mutator.probabilistically_apply_mutation`
        """
        mutation_level = "value" if gene_params.get("mutation_level") != "gene" else "gene"

        if is_list_type(gene_params) and mutation_level == "value":
            return [self.probabilistically_apply_mutation(value, gene_params) for value in gene]

        return self.probabilistically_apply_mutation(gene, gene_params)

    def probabilistically_apply_mutation(self, target, gene_params):
        """
        Either applies a mutation function to a target (gene or value of a gene) or does not, probabilistically according to the ``mutation_rate``

        :param target: the target to which to apply the mutation
        :type target: a valid, non-list, gene type

        :param gene_params: parameters for a single gene; see :ref:`genome-params`
        :type gene_params: dict


        :returns: either the mutated target or the original target


        Dependencies:
            * :func:`~holland.utils.utils.bound_value`
        """
        mutation_function = gene_params["mutation_function"]
        mutation_rate = gene_params["mutation_rate"]
        should_bound = is_numeric_type(gene_params)
        to_int = gene_params.get("type") in ["int", "[int]"]
        minimum = gene_params.get("min")
        maximum = gene_params.get("max")

        if random.random() < mutation_rate:
            mutated_target = mutation_function(target)
            if should_bound:
                if isinstance(target, list):
                    mutated_target = [
                        bound_value(value, minimum=minimum, maximum=maximum, to_int=to_int)
                        for value in mutated_target
                    ]
                else:
                    mutated_target = bound_value(
                        mutated_target, minimum=minimum, maximum=maximum, to_int=to_int
                    )
            return mutated_target
        return target
