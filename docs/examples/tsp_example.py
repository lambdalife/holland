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