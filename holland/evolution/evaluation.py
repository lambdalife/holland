def evaluate_fitness(gene_pool, fitness_function):
    """
    Evaluates the fitness of a population

    :param gene_pool: a population to evaluate
    :type gene_pool: list

    :returns: a list of tuples of the form ``(score, genome)``.

	.. todo:: write an example
    """

    results = []
    for genome in gene_pool:
        score = fitness_function(genome)
        results.append((score, genome))
    return results
