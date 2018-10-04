def cross(parent_genomes, genome_params):
    """
    Crosses the genome of a given list of parents

    .. note:: Holland generalizes the usual 2 parent crossover and supports k-parent crossover

    :param parent_genomes: a list of parents
    :type parent_geomes: list

    :param genome_params: a dictionary specifying genome parameters
    :type genome_params: dict


    :returns: a single genome based on the parent genomes


    Dependencies:
        * :ref:`crossover-functions`
    """
    offspring = {}
    for gene_name in parent_genomes[0].keys():
        crossover_function = genome_params[gene_name]["crossover_function"]
        parent_genes = [pg[gene_name] for pg in parent_genomes]
        offspring[gene_name] = crossover_function(parent_genes)

    return offspring
