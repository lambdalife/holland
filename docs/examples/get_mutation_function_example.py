import random


mutate = get_some_mutation_function()
genome = {"gene1": [123.8, 118.2, 103.0], "gene2": [1.5, 3.7, 2.6, 1.9]}
mutation_rate = 0.01

mutated_genome = {}
for gene_name, gene in genome:
    mutated_gene = [
        mutate(value) if random.random() < mutation_rate else value  # apply probabilistically
        for value in gene
    ]
    mutated_genome[gene_name] = mutated_gene
