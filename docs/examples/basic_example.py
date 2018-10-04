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