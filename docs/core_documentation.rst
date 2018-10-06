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
.. autofunction:: holland.evolution.cross_genomes


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
.. autofunction:: holland.library.get_flip_mutator
.. autofunction:: holland.library.get_boundary_mutator
.. autofunction:: holland.library.get_uniform_mutator
.. autofunction:: holland.library.get_gaussian_mutator



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



.. _fitness-function:

Fitness Function
----------------

The fitness function is a user-written function that maps genomes to fitness scores, which in turn, are used in breeding the next generation. A fitness function must accept a single genome and return an integer or float corresponding to the fitness of the given genome. See :func:`~holland.evolution.evaluate_fitness` for details on how the fitness function is used.

Holland is designed to be application-agnostic, so a fitness function can evaluate a genome in any way so long as the input and output match what is expected. A fitness function might simply plug in different values from a genome's genes into a formula or it might create an instance of some class according to the parameters specified in the genome and then run a simulation for that individual.

Example:
    .. literalinclude:: examples/fitness_function_example.py


.. _genome-params:

Genome Parameters
-----------------

In order to generate initial and random genomes, perform crossover on genomes, and mutate genomes, ``genome_params`` are required to be specifed. The structure of genomes for populates are determined by these parameters. ``genome_params`` is a dictionary whose keys correspond to individual genes, where the dictionary contained at each key specifies parameters for that gene.

This is an example of ``genome_params``::

    {
        "gene1": {
            "type": "float",
            "size": 100,
            "max": 100000,
            "min": -100000,
            "initial_distribution": lambda: random.uniform(-100000, 100000),
            "crossover_function": get_point_crossover_function(num_crossover_points=3),
            "mutation_function": get_gaussian_mutation_function(100),
            "mutation_rate": 0.01
        },
        "gene2": {
            "type": "bool",
            "size": 5,
            "initial_distribution": lambda: random.random() < 0.5,
            "crossover_function": get_uniform_crossover_function(),
            "mutation_function": get_flip_mutation_function(),
            "mutation_rate": 0.05
        }
    }

The significance of these values is as follows:

    * **type** (*str*) -- specifies the type of the gene (options: ``"float"``, ``"bool"``)
    * **size** (*int*) -- specifies the length of the gene
    * **max** (*int/float*) -- specifies the maximum allowed value for any element of the gene
    * **min** (*int/float*) -- specifies the minimum allowed value for any element of the gene
    * **initial_distribution** (*func*) -- a function for initializing a random gene with values; must not accept any positional arguments
    * **crossover_function** (*func*) -- a function to cross multiple parent genes; see :ref:`crossover-functions` for more
    * **mutation_function** (*func*) -- a function that mutates a single value of a gene; see :ref:`mutation-functions` for more
    * **mutation_rate** (*int/float*) -- probability (``0`` to ``1``) that each value of the gene gets mutated (by applying the ``mutation_function``)

Note that each gene may contain values of only one type.


.. _selection-strategy:

Selection Strategy
------------------

The selection strategy for breeding the next generation of indviduals is specified in the ``selection_strategy`` dictionary. The strategy is ultimately used by the functions :func:`~holland.evolution.select_breeding_pool`, which uses information contained in the ``"pool"`` section of the selection strategy, and :func:`~holland.evolution.select_parents`, which uses information contained in ``"parents"``.

The dictionary ``selection_strategy`` should have the below form. The example values shown here are the defaults and any parameters that are not specified will use these values as defaults::

    {
        "pool": {
            "top": 0,
            "mid": 0,
            "bottom": 0,
            "random": 0
        },
        "parents": {
            "weighting_function": lambda x: 1,
            "number": 2
        }
    }

The significance of these values is as follows:
    
    * **pool**
        * **top** (*int*) -- number of genomes to select from the top (end) of the pack (by fitness)
        * **mid** (*int*) -- number of genomes to select from the middle of the pack (by fitness)
        * **bottom** (*int*) -- number of genomes to select from the bottom (start) of the pack (by fitness)
        * **random** (*int*) -- number of genomes to select at random
    * **parents**
        * **weighting_function** (*func*) -- function for converting a fitness score into a probability for selecting an individual as a parent (default is even weighting)
        * **number** (*int*) -- number of parents to select for each offspring




.. _fitness-storage-options:

Fitness Storage Options
-----------------------

To measure performance improvements over the generations, fitness statistics can be stored for each generation. If enabled, the statistics recorde are max, min, mean, median, and standard deviation. Values can be stored either to a file (csv) or in memory and returned by :func:`~holland.evolution.evolve`. By default fitness statistics are not recorded.

The following options are available:

    * **should_record_fitness** (*bool*) – determines whether or not to record fitness
    * **file_name** (*str*) – name of the file to write to
    * **format** (*str*) – file format (options: 'csv', 'memory'); if 'memory', stats are returned as second element of tuple in :func:`~holland.evolution.evolve`
    * **path** (*str*) – location of the file to write

See the :ref:`storage-fitness` subsection of :ref:`storage` for more on how these values are used.



.. _genome-storage-options:

Genome Storage Options
----------------------

To record snapshots of the population over the generations genomes and their corresponding fitness scores (in the same format returned by :func:`~holland.evolution.evaluate_fitness`) can be recorded. If enabled, individuals will be selected according to the specified strategy and stored to a file (json). Additionally, by setting ``should_record_on_interrupt`` to ``True`` (which is independent of the value of ``should_record_genomes``), genomes will be recorded if an unhandled exception is thrown during execution. By default genomes are not recorded.

The following options are available:

    * **should_record_genomes** (*bool*) – determines wether or not to record genomes at all
    * **record_every_n_generations** (*int*) – recording frequency
    * **should_record_on_interrupt** (*bool*) – determines wether or not to record genomes if an unhandled exception (including KeyboardInterrupt) is raised
    * **should_add_generation_suffix** (*bool*) – determines whether or not to append '-generation_{n}' to the end of file_name
    * **file_name** (*str*) – name of the file to write to
    * **format** (*str*) – file format (options: 'json')
    * **path** (*str*) – location of the file to write
    * **top** (*int*) – number of genomes and scores to select from the top of the pack (by fitness)
    * **mid** (*int*) – number of genomes and scores to select from the middle of the pack (by fitness)
    * **bottom** (*int*) – number of genomes and scores to select from the bottom of the pack (by fitness)

See the :ref:`storage-genomes-and-fitnesses` subsection of :ref:`storage` for more on how these values are used.


.. _crossover-functions:

Crossover Functions
-------------------

Crossover functions are used to splice parent genes together to form a gene for an offspring. Crossover functions can be custom made, but Holland offers a few common crossover functions built in, these are described in the :ref:`library-crossover-functions` subsection of :ref:`library`. If you write or find a novel crossover function that you find useful, consider contributing it to the Holland library!

Crossover functions act on, and are specified for, individual genes, rather than entire genomes. Since Holland supports reproduction between an arbitrary number of individuals (parents) crossover functions must accept a single argument: a list containing parent gene(s). The length of this list is determined by the number of parents as specified in the ``selection_strategy`` (see :ref:`selection-strategy`). Crossover functions must return a single gene.

Example:
    .. literalinclude:: examples/crossover_function_example.py


.. _mutation-functions:

Mutation Functions
------------------

Mutation functions are used to modify gene values. Like :ref:`crossover-functions`, mutation functions can be custom made, but Holland offers a few common mutation functions built in, these are described in the :ref:`library-mutation-functions` subsection of :ref:`library`. If you write or find a novel mutation function that you find useful, consider contributing it to the Holland library!

Mutation functions act on individual values of a gene, rather than entire genes or genomes. Mutation functions are specified for each gene. A mutation function is applied probabilistically (by :func:`~holland.evolution.probabilistically_mutate_value`), and, therefore, need not consider the ``mutation_rate`` for the gene. Mutation functions must return the mutated value.

Example:
    .. literalinclude:: examples/mutation_function_example.py
