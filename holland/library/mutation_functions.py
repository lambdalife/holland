import random


def get_flip_mutator():
    return lambda value: not value


def get_boundary_mutator(minimum, maximum):
    return lambda value: minimum if random.random() < 0.5 else maximum


def get_uniform_mutator(minimum, maximum):
    return lambda value: random.uniform(minimum, maximum)


def get_gaussian_mutator(sigma):
    return lambda value: random.gauss(value, sigma)
