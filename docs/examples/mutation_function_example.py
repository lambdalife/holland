import random


def mutate_value(value):
    """Randomly doubles or halves a value -- applied at "value" level"""
    if random.random() < 0.5:
        return value * 2
    return value / 2


def mutate_gene(gene):
    """Shuffle a gene -- applied at "gene" level"""
    random.shuffle(gene)
    return gene
