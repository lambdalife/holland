def crossover(parent_genes):
    """Take each value by alternating between parent genes"""
    num_parents = len(parent_genes)
    gene_length = len(parent_genes[0])
    return [parent_genes[i % num_parents][i] for i in range(gene_length)]
