Core Documentation
==================

Here is the core documentation for Holland

.. contents::
	:local:
	:depth: 2

Evolution
---------

evolution
~~~~~~~~~
.. autofunction:: holland.evolution.evolve

breeding
~~~~~~~~
.. autofunction:: holland.evolution.generate_next_generation
.. autofunction:: holland.evolution.breed_next_generation
.. autofunction:: holland.evolution.generate_random_genomes


crossover
~~~~~~~~~
.. autofunction:: holland.evolution.cross


evaluation
~~~~~~~~~~
.. autofunction:: holland.evolution.evaluate_fitness


mutation
~~~~~~~~
.. autofunction:: holland.evolution.mutate_genome
.. autofunction:: holland.evolution.mutate_gene
.. autofunction:: holland.evolution.probabilistically_mutate_value


selection
~~~~~~~~~
.. autofunction:: holland.evolution.select_breeding_pool
.. autofunction:: holland.evolution.select_parents



Library
-------

crossover functions
~~~~~~~~~~~~~~~~~~~
.. autofunction:: holland.library.get_uniform_crossover_function
.. autofunction:: holland.library.get_point_crossover_function

mutation functions
~~~~~~~~~~~~~~~~~~
.. autofunction:: holland.library.get_flip_mutator
.. autofunction:: holland.library.get_boundary_mutator
.. autofunction:: holland.library.get_uniform_mutator
.. autofunction:: holland.library.get_gaussian_mutator



Storage
-------

fitness
~~~~~~~
.. autofunction:: holland.storage.record_fitness
.. autofunction:: holland.storage.format_fitness_statistics

genomes and fitnesses
~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: holland.storage.record_genomes_and_fitnesses
.. autofunction:: holland.storage.format_genomes_and_fitnesses_for_storage

utils
~~~~~
.. autofunction:: holland.storage.record
.. autofunction:: holland.storage.record_to_csv
.. autofunction:: holland.storage.record_to_json



Utils
-----

utility functions
~~~~~~~~~~~~~~~~~
.. autofunction:: holland.utils.bound_value
.. autofunction:: holland.utils.select_from



Genome Parameters
-----------------

Holland supports the three basic types for each gene: boolean, int, float. Each gene can hold a single value of one type, or a list of one type.

Holland enforces strong typing.
* boolean/[boolean]
* int/[int] - requires min/max
* float/[float] - requires min/max


.. _mutation-functions

Mutation Functions
------------------

.. _crossover-functions:

Crossover Functions
-------------------
Crossover function guide
