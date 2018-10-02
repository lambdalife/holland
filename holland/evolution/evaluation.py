def evaluate_fitness(gene_pool, fitness_function):
    results = []
    for genome in gene_pool:
        score = fitness_function(genome)
        results.append((score, genome))
    return results
