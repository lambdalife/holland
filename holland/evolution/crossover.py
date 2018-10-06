def cross_genomes(parent_genomes, genome_params):
    """
    Produces a new genome by applying crossover to multiple parent genomes

    .. note:: Holland generalizes the usual 2 parent crossover and supports k-parent crossover

    :param parent_genomes: a list of parent genomes
    :type parent_geomes: list

    :param genome_params: a dictionary specifying genome parameters, specifcally ``crossover_function`` is relevant; see :ref:`genome-params`
    :type genome_params: dict


    :returns: a single genome

    """
    offspring = {}
    for gene_name in parent_genomes[0].keys():
        parent_genes = [pg[gene_name] for pg in parent_genomes]
        crossover_function = genome_params[gene_name]["crossover_function"]
        offspring[gene_name] = crossover_function(parent_genes)

    return offspring
