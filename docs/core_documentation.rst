Core Documentation
==================

Here is the core documentation for Holland

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



Utils
-----
.. autofunction:: holland.utils.bound_value