<h1 align='center'>Holland</h1>
<h2 align='center'>Genetic Algorithm Library for Python</h1>

> Computer programs that "evolve" in ways that resemble natural selection can solve complex problems even their creators do not fully understand - John H. Holland

<div align='center'>
    <a href="https://github.com/henrywoody/holland/blob/master/LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
    <a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</div>

### Description

This is a package for implementing the Genetic Algorithm in Python. The program is designed to act on an arbitrary evaluation function with arbitrary encoding of individuals within a population, both of which are provided by the user.

Holland handles the reproduction step of the Genetic Algorithm and can be configured to work in a variety of ways.

Holland also manages saving genomes for individuals and populations as well as plotting fitness over time.

### Usage
Full documentation on [ReadTheDocs](hollandpy.readthedocs.io).

**Basic Example**

```python
from holland import evolve
from math import cos, pi

# specify hyper-parameters for genomes
genome_parameters = {
    'gene1': {
        'type': 'float',
        'min': -pi,
        'max': pi
    },
    'gene2': {
        'type': 'float',
        'min': -pi,
        'max': pi
    }
}

# define a fitness function
def my_fitness_function(individual):
    return cos(inidividual.gene1)*cos(individual.gene2)

# evolve!
my_population = holland.evolve(genome_parameters,
                               fitness_function = my_fitness_function,
                               show_fitness_plot = True,
                               num_generations = 100)
```

A more complex example

**TSP**

```python
from holland import evolve
from math import sqrt

# list of cities and positions
cities = {
    'AZ': (1,2),
    'CA': (4,6),
    'NM': (0,3)
}

# specify hyper-parameters for genomes
genome_parameters = {
    'path': {
        'type': '[string]',
        'possible_values': ['AZ', 'CA', 'NM'],
        'mutation_function': 'swap'
    }
}

def distance(p1, p2):
	dx = p1[0]-p2[0]
	dy = p1[1]-p2[1]
	return sqrt(dx*dx + dy*dy)

# define a fitness function
def sum_of_distances(individual):
    return sum([
    	distance(city_1, city_2)
        for (city_1, city_2)
        in zip(c, c[1:])
    ])

# evolve!
my_population = holland.evolve(genome_parameters,
                               fitness_function = my_fitness_function,
                               anneal_mutation_rate = True,
                               show_fitness_plot = True,
                               num_generations = 100)
```
