crossover = get_some_crossover_function()

parent_genomes = select_parents(fitness_results)
gene_names = parent_genomes[0].keys()

offspring = {}
for gene_name in gene_names:
    parent_genes = [pg[gene_name] for pg in parent_genomes]
    offspring[gene_name] = crossover(parent_genes)
