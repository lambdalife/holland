def evaluate_fitness(gene_pool, fitness_function, ascending=True):
    """
    Evaluates the fitness of a population by applying a fitness function to each genome in the population

    :param gene_pool: a population of genomes to evaluate
    :type gene_pool: list

    :param fitness_function: a function for evaluating the fitness of each genome; see :ref:`fitness-function`
    :type fitness_function: func

    :param ascending: whether or not to sort results in ascending order of fitness
    :type ascending: bool


    :returns: a sorted list of tuples of the form ``(score, genome)``.

    """

    results = []
    for genome in gene_pool:
        score = fitness_function(genome)
        results.append((score, genome))
    return sorted(results, key=lambda x: x[0], reverse=(not ascending))
