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
.. autoclass:: holland.evolution.Evolver
	:members:


evaluation
~~~~~~~~~~
.. autoclass:: holland.evolution.Evaluator
	:members:


breeding
~~~~~~~~
.. autoclass:: holland.evolution.PopulationGenerator
	:members:


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

.. _library-fitness-weighting-functions:

fitness weighting functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fitness weighting functions are used by :func:`~holland.evolution.Selector.select_parents` to weight fitness scores and generate probabilities for selecting a genome to be a parent of a genome in the next generation. The following functions return stock weighting functions, some with configurable parameters. See :ref:`selection-strategy` for general information.

General Example:

    .. literalinclude:: examples/get_fitness_weighting_function_example.py
        :emphasize-lines: 4,10


.. automodule:: holland.library.fitness_weighting_functions
	:members:


.. _library-crossover-functions:

crossover functions
~~~~~~~~~~~~~~~~~~~

Crossover functions are used by :func:`~holland.evolution.Crosser.cross_genomes` to perform crossover. The following functions return stock crossover functions, some with configurable parameters. See :ref:`crossover-functions` for general information.

General Example:
	
	.. literalinclude:: examples/get_crossover_function_example.py
		:emphasize-lines: 1,9

.. automodule:: holland.library.crossover_functions
	:members:

.. _library-mutation-functions:

mutation functions
~~~~~~~~~~~~~~~~~~

Mutation functions are used by :func:`~holland.evolution.Mutator.probabilistically_apply_mutation` to apply mutation to a gene value. The following functions return stock mutation functions, some with configurable parameters. See :ref:`mutation-functions` for general information.

General Example:
	
	.. literalinclude:: examples/get_mutation_function_example.py
		:emphasize-lines: 4,11

.. automodule:: holland.library.mutation_functions
	:members:




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
.. automodule:: holland.storage.fitness
	:members:


.. _storage-genomes-and-fitnesses:

genomes and fitnesses
~~~~~~~~~~~~~~~~~~~~~
.. automodule:: holland.storage.genomes_and_fitnesses
	:members:


.. _storage-utils:

utils
~~~~~
.. automodule:: holland.storage.utils
	:members:



Utils
-----

utility functions
~~~~~~~~~~~~~~~~~
.. automodule:: holland.utils.utils
	:members:
