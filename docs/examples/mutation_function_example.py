import random


def mutate(value):
    """Randomly doubles or halves a value"""
    if random.random() < 0.5:
        return value * 2
    return value / 2
