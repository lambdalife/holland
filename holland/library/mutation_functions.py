import random


def get_flip_mutation_function():
    """
    Returns a function that returns the negated value of the input, where the input is a boolean value; see :ref:`mutation-functions`
    
    :Valid For:
        ``"bool"`` and ``"[bool]"`` gene types


    :returns: a function that returns the negated value if its input


    Example::
        
        import random


        genome = {
            "gene1": [True, True, False, True, False, False, False],
            "gene2": [False, False, True, False]
        }
        flip_mutate = get_flip_mutation_function()
        mutation_rate = 0.01
    
        mutated_genome = {}
        for gene_name, gene in genome:
            mutated_gene = [
                flip_mutate(value) if random.random() < mutation_rate else value #apply probabilistically
                for value in gene
            ]
            mutated_genome[gene_name] = mutated_gene

    """
    return lambda value: not value


def get_boundary_mutation_function(minimum, maximum):
    """
    Returns a function that pushes a value to either the minimum or maximum allowed value for a gene; see :ref:`mutation-functions`

    :Valid For:
        ``"int"``, ``"[int]"``, ``"float"``, and ``"[float]"`` gene types

    :param minimum: the minimum allowed value
    :type minimum: int/float

    :param maximum: the maximum allowed value
    :type maximum: int/float


    :returns: either ``minimum`` or ``maximum`` (equally likely)


    Example::

        import random


        genome = {
            "gene1": [123.8, 118.2, 103.0],
            "gene2": [1.5, 3.7, 2.6, 1.9]
        }
        minimum = 0
        maximum = 1000
        boundary_mutate = get_boundary_mutation_function(minimum, maximum)
        mutation_rate = 0.01
    
        mutated_genome = {}
        for gene_name, gene in genome:
            mutated_gene = [
                boundary_mutate(value) if random.random() < mutation_rate else value #apply probabilistically
                for value in gene
            ]
            mutated_genome[gene_name] = mutated_gene
    """
    return lambda value: minimum if random.random() < 0.5 else maximum


def get_uniform_mutation_function(minimum, maximum):
    """
    Returns a function that returns a value drawn from a uniform distribution over the closed interval [minimum, maximum]; see :ref:`mutation-functions`

    :Valid For:
        any gene type

    :param minimum: the minimum allowed value
    :type minimum: int/float

    :param maximum: the maximum allowed value
    :type maximum: int/float


    :returns: a sample from a uniform distribution


    Example::

        import random


        genome = {
            "gene1": [123.8, 118.2, 103.0],
            "gene2": [1.5, 3.7, 2.6, 1.9]
        }
        minimum = 0
        maximum = 1000
        uniform_mutate = get_uniform_mutation_function(minimum, maximum)
        mutation_rate = 0.01
    
        mutated_genome = {}
        for gene_name, gene in genome:
            mutated_gene = [
                uniform_mutate(value) if random.random() < mutation_rate else value #apply probabilistically
                for value in gene
            ]
            mutated_genome[gene_name] = mutated_gene
    """
    return lambda value: random.uniform(minimum, maximum)


def get_gaussian_mutation_function(sigma):
    """
    Returns a function that returns a value drawn from a gaussian (normal) distribution with mean equal to ``value`` and standard_deviation equal to ``sigma``

    :Valid For:
        ``"int"``, ``"[int]"``, ``"float"``, and ``"[float]"`` gene types

    :param sigma: standard deviation for the gaussian distribution
    :type sigma: int/float


    :returns: a sample from a gaussian distribution


    Example::

        import random


        genome = {
            "gene1": [123.8, 118.2, 103.0],
            "gene2": [1.5, 3.7, 2.6, 1.9]
        }
        sigma = 50
        gaussian_mutate = get_gaussian_mutation_function(sigma)
        mutation_rate = 0.01
    
        mutated_genome = {}
        for gene_name, gene in genome:
            mutated_gene = [
                gaussian_mutate(value) if random.random() < mutation_rate else value #apply probabilistically
                for value in gene
            ]
            mutated_genome[gene_name] = mutated_gene
    """
    return lambda value: random.gauss(value, sigma)
