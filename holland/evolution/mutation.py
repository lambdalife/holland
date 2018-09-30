import random


def mutate_genome(genome, genome_params):
    return {
        gene_name: mutate_gene(genome[gene_name], genome_params[gene_name])
        for gene_name in genome.keys()
    }


def mutate_gene(gene, gene_params):
    mutation_function = gene_params["mutation_function"]
    mutation_rate = gene_params["mutation_rate"]
    return [
        probabilistically_mutate_value(
            value, mutation_function, mutation_rate=mutation_rate
        )
        for value in gene
    ]


def probabilistically_mutate_value(value, mutation_function, mutation_rate=0.001):
    if random.random() < mutation_rate:
        return mutation_function(value)
    return value
