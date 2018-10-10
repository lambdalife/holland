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


selection
~~~~~~~~~
.. autoclass:: holland.evolution.Selector
	:members:


crossover
~~~~~~~~~
.. autoclass:: holland.evolution.Crosser
	:members:


mutation
~~~~~~~~
.. autoclass:: holland.evolution.Mutator
	:members:



.. _library:

Library
-------

.. _library-crossover-functions:

crossover functions
~~~~~~~~~~~~~~~~~~~

Crossover functions are used by :func:`~holland.evolution.cross_genomes` to perform crossover. The following functions return stock crossover functions, some with configurable parameters. See :ref:`crossover-functions` for general information.

General Example:
	
	.. literalinclude:: examples/get_crossover_function_example.py
		:emphasize-lines: 1,9

.. autofunction:: holland.library.get_uniform_crossover_function
.. autofunction:: holland.library.get_point_crossover_function
.. autofunction:: holland.library.get_and_crossover_function
.. autofunction:: holland.library.get_or_crossover_function

.. _library-mutation-functions:

mutation functions
~~~~~~~~~~~~~~~~~~

Mutation functions are used by :func:`~holland.evolution.probabilistically_mutate_value` to apply mutation to a gene value. The following functions return stock mutation functions, some with configurable parameters. See :ref:`mutation-functions` for general information.

General Example:
	
	.. literalinclude:: examples/get_mutation_function_example.py
		:emphasize-lines: 4,11

.. autofunction:: holland.library.get_flip_mutation_function
.. autofunction:: holland.library.get_boundary_mutation_function
.. autofunction:: holland.library.get_uniform_mutation_function
.. autofunction:: holland.library.get_gaussian_mutation_function

.. _library-fitness-weighting-functions:

fitness weighting functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fitness weighting functions are used by :func:`~holland.evolution.select_parents` to weight fitness scores and generate probabilities for selecting a genome to be a parent of a genome in the next generation. The following functions return stock weighting functions, some with configurable parameters. See :ref:`selection-strategy` for general information.

General Example:

    .. literalinclude:: examples/get_fitness_weighting_function_example.py
        :emphasize-lines: 4,10


.. autofunction:: holland.library.get_uniform_weighting_function
.. autofunction:: holland.library.get_linear_weighting_function
.. autofunction:: holland.library.get_polynomial_weighting_function
.. autofunction:: holland.library.get_exponential_weighting_function
.. autofunction:: holland.library.get_logarithmic_weighting_function
.. autofunction:: holland.library.get_reciprocal_weighting_function




.. _storage:

Storage
-------

.. _storage-manager:

storage manager
~~~~~~~~~~~~~~~
.. autoclass:: holland.storage.StorageManager
	:members:


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
.. autofunction:: holland.utils.is_numeric_type
