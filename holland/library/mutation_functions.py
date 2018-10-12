import random


def get_flip_mutation_function():
    """
    Returns a function that returns the negated value of the input, where the input is a boolean value; see :ref:`mutation-functions`
    
    :Valid For:
        ``"bool"`` and ``"[bool]"`` gene types


    :returns: a function that returns the negated value if its input
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
    """
    return lambda value: random.uniform(minimum, maximum)


def get_gaussian_mutation_function(sigma):
    """
    Returns a function that returns a value drawn from a gaussian (normal) distribution with mean equal to ``value`` and standard_deviation equal to ``sigma``; see :ref:`mutation-functions`

    :Valid For:
        ``"int"``, ``"[int]"``, ``"float"``, and ``"[float]"`` gene types

    :param sigma: standard deviation for the gaussian distribution
    :type sigma: int/float


    :returns: a sample from a gaussian distribution
    """
    return lambda value: random.gauss(value, sigma)
