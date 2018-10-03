API Reference
=============

.. contents:: Table of Contents


Main Functions
--------------

.. method:: evolve(genome_params, fitness_functions[, initial_population][, population_size = 100][, anneal_mutation_rate = False[, annealing_rate = 0.01]][, show_fitness_plot = True][, num_generations = 100])

   :param genome_params: hyper-parameters for genomes
   :param fitness_function: fitness function
   :param initial_population: an optional list of individuals to use as the starting population.
   :param anneal_mutation_rate: whether to decrease the mutation rate over time or not
   :param annealing_rate: specifies :math:`\alpha` in the annealing equation :math:`e^{\alpha(s-s')/T}`.
   :param show_fitness_plot: whether to plot max, min, and avg fitness per generation
   :param num_generations: the number of generations to evolve

.. note:: If no ``initial_population`` is supplied, then an initial population is randomly generated. However if ``initial_population`` *is* supplied but the genome of an individual does not match the given ``genome_params``, an error is thrown. However, if only some parameters are supplied, then the missing parameters will be randomly generated.

.. warning:: If you use our library you may experience sudden death