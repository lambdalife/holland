Basic Usage
===========

.. contents:: Table of Contents

First example
-------------

Getting started with Holland is easy. Simply define your genome encoding and fitness function to get started

.. code-block:: python

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
	my_population = evolve(genome_parameters,
		fitness_function = my_fitness_function,
		show_fitness_plot = True,
		num_generations = 100)


Intermediate Example: TSP
-------------------------

.. code-block:: python

	from holland import evolve
	from math import sqrt

	# list of cities and positions
	cities = {
		'AZ': (1,2),
		'CA': (3,4),
		'NM': (5,6),
		'TX': (7,8)
	}

	# specify hyper-parameters for genomes
	# in this case there is only a single gene
	genome_parameters = {
		'path': {
			'type': '[string]',
			'possible_values': cities.keys(),
			'mutation_function': 'swap'
		}
	}

	def distance(p1, p2):
		dx = p1[0]-p2[0]
		dy = p1[1]-p2[1]
		return sqrt(dx*dx + dy*dy)

	# define a fitness function
	# a pythonic way to find the length of a round trip
	def sum_of_distances(individual):
		cities = [position[city] for city in individual['path']]
		return sum([
			distance(city_1, city_2)
			for (city_1, city_2)
			in zip(cities, cities[1:]+[cities[0]])
		])

	# evolve!
	my_population = evolve(genome_parameters,
		fitness_function = my_fitness_function,
		anneal_mutation_rate = True,
		show_fitness_plot = True,
		num_generations = 100)