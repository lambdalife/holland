class Evaluator:
    """
    Handles evaluation of genomes

    :param fitness_function: a function for evaluating the fitness of each genome; see :ref:`fitness-function`
    :type fitness_function: func

    :param ascending: whether or not to sort results in ascending order of fitness
    :type ascending: bool
    """

    def __init__(self, fitness_function, ascending=True):
        self.fitness_function = fitness_function
        self.ascending = ascending

    def evaluate_fitness(self, gene_pool):
        """
        Evaluates the fitness of a population by applying a fitness function to each genome in the population

        :param gene_pool: a population of genomes to evaluate
        :type gene_pool: list


        :returns: a sorted list of tuples of the form ``(score, genome)``.
        """
        results = []
        for genome in gene_pool:
            result = self.fitness_function(genome)
            if type(result) in [list, tuple]:
                results.append(result)
            else:
                results.append((result, genome))
        return sorted(results, key=lambda x: x[0], reverse=(not self.ascending))
