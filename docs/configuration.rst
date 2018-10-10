Configuration
=============

This page provides information on configuring Holland, specifically initializing the :class:`~holland.evolution.Evolver` class and using its :func:`~holland.evolution.Evolver.evolve` method.

.. contents::
    :local:
    :depth: 2


.. _fitness-function:

Fitness Function
----------------

The fitness function is a user-written function that maps genomes to fitness scores, which in turn, are used in breeding the next generation. A fitness function must accept a single genome and return an integer or float corresponding to the fitness of the given genome. See :func:`~holland.evolution.Evaluator.evaluate_fitness` for details on how the fitness function is used.

Holland is designed to be application-agnostic, so a fitness function can evaluate a genome in any way so long as the input and output match what is expected. A fitness function might simply plug in different values from a genome's genes into a formula or it might create an instance of some class according to the parameters specified in the genome and then run a simulation for that individual.

Example:
    .. literalinclude:: examples/fitness_function_example.py



.. _genome-params:

Genome Parameters
-----------------

In order to generate initial and random genomes, perform crossover on genomes, and mutate genomes, ``genome_params`` are required to be specifed. The structure of genomes for populates are determined by these parameters. ``genome_params`` is a dictionary whose keys correspond to individual genes, where the dictionary contained at each key specifies parameters for that gene.

Each gene must have a specified type. There are two broad categories of gene types: list-types and value-types. List-type genes are lists of a set length and containing only elements of a single type. Value-type genes are single values. List-type genes use the notation ``"[type]"`` while value-type genes use the notation ``"type"``.

This is an example of ``genome_params``::

    {
        "gene1": {
            "type": "int",
            "max": 100000,
            "min": -100000,
            "initial_distribution": lambda: random.uniform(-100000, 100000),
            "crossover_function": get_uniform_crossover_function(),
            "mutation_function": get_gaussian_mutation_function(100),
            "mutation_rate": 0.01
        },
        "gene2": {
            "type": "[float]",
            "size": 100,
            "max": 100000,
            "min": -100000,
            "initial_distribution": lambda: random.uniform(-100000, 100000),
            "crossover_function": get_point_crossover_function(n_crossover_points=3),
            "mutation_function": get_gaussian_mutation_function(100),
            "mutation_rate": 0.01
        },
        "gene3": {
            "type": "bool",
            "initial_distribution": lambda: random.random() < 0.5,
            "crossover_function": get_uniform_crossover_function(),
            "mutation_function": get_flip_mutation_function(),
            "mutation_rate": 0.05
        },
        "gene4": {
            "type": "[str]",
            "size": 5,
            "initial_distribution": lambda: random.sample(list_of_words, 1)[0],
            "crossover_function": get_uniform_crossover_function(),
            "mutation_function": rotate_order,
            "mutation_level": "gene",
            "mutation_rate": 0.05
        }
    }

The significance of these values is as follows:

    * **type** (*str*) -- specifies the type of the gene; if the gene is just a single value, use the plain type, but if the gene is a list of values, use the type in brackets; options:

        * ``"float"``, ``"[float]"``
        * ``"int"``, ``"[int]"``
        * ``"bool"``, ``"[bool]"``
        * ``"str"``, ``"[str]"``

    * **size** (*int*) -- specifies the length of the gene if list-type
    * **max** (*int/float*) -- specifies the maximum allowed value for the gene or any element of the gene if of a numeric type
    * **min** (*int/float*) -- specifies the minimum allowed value for the gene or any element of the gene if of a numeric type
    * **initial_distribution** (*func*) -- a function for initializing a random gene with values; must not accept any positional arguments
    * **crossover_function** (*func*) -- a function to cross multiple parent genes; see :ref:`crossover-functions` for more
    * **mutation_function** (*func*) -- a function that mutates either the whole gene or a single value of the gene (depending on ``mutation_level``); see :ref:`mutation-functions` for more
    * **mutation_level** (*str*) -- specifies how to apply the ``mutation_funtion``: either to the gene as a whole, or just individual values; default is ``"value"`` (options: ``"value"``, ``"gene"``); irrelevant for value-type genes
    * **mutation_rate** (*int/float*) -- probability (``0`` to ``1``) that each value of the gene gets mutated (by applying the ``mutation_function``)



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

Mutation functions can act on either individual values of a gene or an entire gene, but not the whole genome. Mutation functions are specified for each gene. To have a mutation function applied to a whole gene (when the gene is a list-type), the option ``"mutation_level"`` should be set to ``"gene"`` instead of ``"value"`` (see :ref:`genome-params` for more detail); for value-type genes this distinction does not matter. For most applications of the Genetic Algorithm a ``"mutation_level"`` of ``"value"`` should be appropriate, but some applications---e.g. Travelling Salesman---require mutations be applied at the gene level.

A mutation function is applied probabilistically (by :func:`~holland.evolution.Mutator.probabilistically_apply_mutation`), and, therefore, need not consider the ``mutation_rate`` of the gene. Mutation functions must return the mutated value or gene.

Example:
    .. literalinclude:: examples/mutation_function_example.py



.. _selection-strategy:

Selection Strategy
------------------

The selection strategy for breeding the next generation of indviduals is specified in the ``selection_strategy`` dictionary. The strategy is ultimately used by the functions :func:`~holland.evolution.Selector.select_breeding_pool`, which uses information contained in the ``"pool"`` section of the selection strategy, and :func:`~holland.evolution.Selector.select_parents`, which uses information contained in ``"parents"``.

The fitness weighting function determines how to weight fitness scores in order to translate into probabilities for selection of a genome as a parent for an individual in the next generation. For cases in which fitness is sought to be maximized, an increasing fitness weighting function should be used, whereas  cases in which fitness should be minimized (e.g. fitness represents error) should employ a decreasing fitness weighting function. In both cases a uniform weighting function will suffice. In the case of minimizing fitness, a reciprocal weighting function, linear weighting function with negative slope, or polynomial weighting function with negative power will work. See :ref:`library-fitness-weighting-functions` for stock fitness weighting functions.

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
            "n_parents": 2
        }
    }

The significance of these values is as follows:
    
    * **pool**
        * **top** (*int*) -- number of genomes to select from the top (end) of the pack (by fitness)
        * **mid** (*int*) -- number of genomes to select from the middle of the pack (by fitness)
        * **bottom** (*int*) -- number of genomes to select from the bottom (start) of the pack (by fitness)
        * **random** (*int*) -- number of genomes to select at random
    * **parents**
        * **weighting_function** (*func*) -- function for converting a fitness score into a probability for selecting an individual as a parent (default is uniform weighting); higher weights indicate a higher probability of being selected
        * **n_parents** (*int*) -- number of parents to select for each offspring


.. note:: It is recommended that the ``weighting_function`` return only positive values. While Holland can handle weighting functions that return negative values, this presents an ambiguous case in terms of converting weighted scores to probabilities. Current handling of this case aims to minimally distort probabilities, but results may not be exactly what you expect.


.. _generation-params:

Generation Parameters
---------------------

When creating the population for the next generation, a few optional parameters can be set:

    * **n_random** (*int*) -- number of fully random genomes to introduce to the population in each generation
    * **n_elite** (*int*) -- number of (most fit) genomes to preserve for the next generation
    * **population_size** (*int*) -- size of the population in each generation (required if an initial population is not given)

These values should be placed in the ``generation_params`` dictionary.



.. _fitness-storage-options:

Fitness Storage Options
-----------------------

To measure performance improvements over the generations, fitness statistics can be stored for each generation. If enabled, the statistics recorde are max, min, mean, median, and standard deviation. Values can be stored either to a file (csv) or in memory and returned by :func:`~holland.evolution.Evolver.evolve`. By default fitness statistics are not recorded.

The following options are available:

    * **should_record_fitness** (*bool*) – determines whether or not to record fitness
    * **format** (*str*) – file format (options: 'csv', 'memory'); if 'memory', stats are returned as second element of tuple in :func:`~holland.evolution.Evolver.evolve`
    * **file_name** (*str*) – name of the file to write to
    * **path** (*str*) – location of the file to write

See the :ref:`storage-fitness` subsection of :ref:`storage` for more on how these values are used.



.. _genome-storage-options:

Genome Storage Options
----------------------

To record snapshots of the population over the generations genomes and their corresponding fitness scores (in the same format returned by :func:`~holland.evolution.Evaluator.evaluate_fitness`) can be recorded. If enabled, individuals will be selected according to the specified strategy and stored to a file (json). Additionally, by setting ``should_record_on_interrupt`` to ``True`` (which is independent of the value of ``should_record_genomes``), genomes will be recorded if an unhandled exception is thrown during execution. By default genomes are not recorded.

The following options are available:

    * **should_record_genomes** (*bool*) – determines wether or not to record genomes at all
    * **record_every_n_generations** (*int*) – recording frequency
    * **should_record_on_interrupt** (*bool*) – determines wether or not to record genomes if an unhandled exception (including KeyboardInterrupt) is raised
    * **format** (*str*) – file format (options: 'json')
    * **file_name** (*str*) – name of the file to write to
    * **path** (*str*) – location of the file to write
    * **should_add_generation_suffix** (*bool*) – determines whether or not to append '-generation_{n}' to the end of file_name
    * **top** (*int*) – number of genomes and scores to select from the top of the pack (by fitness)
    * **mid** (*int*) – number of genomes and scores to select from the middle of the pack (by fitness)
    * **bottom** (*int*) – number of genomes and scores to select from the bottom of the pack (by fitness)

See the :ref:`storage-genomes-and-fitnesses` subsection of :ref:`storage` for more on how these values are used.
