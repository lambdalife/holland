def cross(parent_genomes, genome_params):
    offspring = {}
    for gene_name in parent_genomes[0].keys():
        crossover_function = genome_params[gene_name]["crossover_function"]
        parent_genes = [pg[gene_name] for pg in parent_genomes]
        offspring[gene_name] = crossover_function(parent_genes)

    return offspring
