Holland Reference
==================

This page provides the core documentation reference for Holland.

.. contents::
    :local:
    :depth: 2

Evolution
---------

evolution
~~~~~~~~~
.. autofunction:: holland.evolution.evolve


evaluation
~~~~~~~~~~
.. autofunction:: holland.evolution.evaluate_fitness


breeding
~~~~~~~~
.. autofunction:: holland.evolution.generate_next_generation
.. autofunction:: holland.evolution.breed_next_generation
.. autofunction:: holland.evolution.generate_random_genomes


crossover
~~~~~~~~~
.. autofunction:: holland.evolution.cross_genomes


mutation
~~~~~~~~
.. autofunction:: holland.evolution.mutate_genome
.. autofunction:: holland.evolution.mutate_gene
.. autofunction:: holland.evolution.probabilistically_mutate_value


selection
~~~~~~~~~
.. autofunction:: holland.evolution.select_breeding_pool
.. autofunction:: holland.evolution.select_parents



.. _library:

Library
-------

.. _library-crossover-functions:

crossover functions
~~~~~~~~~~~~~~~~~~~
.. autofunction:: holland.library.get_uniform_crossover_function
.. autofunction:: holland.library.get_point_crossover_function

.. _library-mutation-functions:

mutation functions
~~~~~~~~~~~~~~~~~~
.. autofunction:: holland.library.get_flip_mutation_function
.. autofunction:: holland.library.get_boundary_mutation_function
.. autofunction:: holland.library.get_uniform_mutation_function
.. autofunction:: holland.library.get_gaussian_mutation_function



.. _storage:

Storage
-------

.. _storage-fitness:

fitness
~~~~~~~
.. autofunction:: holland.storage.record_fitness
.. autofunction:: holland.storage.format_fitness_statistics

.. _storage-genomes-and-fitnesses:

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
.. autofunction:: holland.utils.is_list_type
