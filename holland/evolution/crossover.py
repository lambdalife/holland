class Crosser:
    """
    Handles genetic crossover

    :param genome_params: a dictionary specifying genome parameters, specifcally ``crossover_function`` is relevant; see :ref:`genome-params`
    :type genome_params: dict
    """

    def __init__(self, genome_params):
        self.genome_params = genome_params

    def cross_genomes(self, parent_genomes):
        """
        Produces a new genome by applying crossover to multiple parent genomes

        :param parent_genomes: a list of parent genomes
        :type parent_geomes: list


        :returns: a single genome
        """
        offspring = {}
        for gene_name in parent_genomes[0].keys():
            parent_genes = [pg[gene_name] for pg in parent_genomes]
            crossover_function = self.genome_params[gene_name]["crossover_function"]
            offspring[gene_name] = crossover_function(parent_genes)

        return offspring
