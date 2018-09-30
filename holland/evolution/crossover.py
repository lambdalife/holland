def cross(genome1, genome2, cross_function):
    return {
        gene_name: cross_function(genome1[gene_name], genome2[gene_name])
        for gene_name in genome1.keys()
    }
