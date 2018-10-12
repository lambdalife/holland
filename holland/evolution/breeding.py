from .selection import Selector
from .crossover import Crosser
from .mutation import Mutator
from ..utils import bound_value, is_numeric_type, is_list_type


class PopulationGenerator:
    """
    Handles generating populations

    :param genome_params: a dictionary specifying genome parameters; see :ref:`genome-params`
    :type genome_params: dict
    
    :param selection_strategy: a dictionary specifying selection parameters; see :ref:`selection-strategy`
    :type selection_strategy: dict
    
    :param generation_params: a dictionary specifying how to create the next generation; see :ref:`generation-params`
    :type generation_params: dict


    :raises ValueError: if ``n_random < 0`` or ``n_elite < 0``
    :raises ValueError: if ``n_random + n_elite > population_size``
    """

    def __init__(self, genome_params, selection_strategy, generation_params={}):
        self.genome_params = genome_params
        self.selection_strategy = selection_strategy

        self.n_random = generation_params.get("n_random", 0)
        self.n_elite = generation_params.get("n_elite", 0)
        self.population_size = generation_params.get("population_size", None)

        if self.n_random < 0 or self.n_elite < 0:
            raise ValueError(
                "Number of random or elite individuals per generation cannot be negative"
            )

        if self.population_size is not None and self.n_random + self.n_elite > self.population_size:
            raise ValueError(
                "Number of random and elite individuals must be less than or equal to population size"
            )

    def generate_next_generation(self, fitness_results):
        """
        Generates the next generation

        :param fitness_results: a sorted list of tuples containing a fitness score in the first position and a genome in the second (returned by :func:`~holland.evolution.Evaluator.evaluate_fitness`)
        :type fitness_results: list


        :returns: a list of genomes

        
        .. note:: For the sake of efficiency, this method expects ``fitness_results`` to be sorted in order to properly select genomes on the basis of fitness. :func:`~holland.evolution.Evaluator.evaluate_fitness` returns sorted results.

        .. todo:: Write an example for usage

        :raises ValueError: if ``n_random + n_elite > population_size``

        Dependencies:
            * :func:`~holland.evolution.PopulationGenerator.breed_next_generation`
            * :func:`~holland.evolution.PopulationGenerator.generate_random_genomes`
        """
        if self.population_size is None:
            self.population_size = len(fitness_results)

        if self.n_random + self.n_elite > self.population_size:
            raise ValueError(
                "Number of random and elite individuals must be less than or equal to population size"
            )

        bred_per_generation = self.population_size - self.n_random - self.n_elite

        if self.n_elite > 0:
            elite_genomes = [genome for fitness, genome in fitness_results[-self.n_elite :]]
        else:
            elite_genomes = []

        bred_genomes = self.breed_next_generation(fitness_results, bred_per_generation)
        random_genomes = self.generate_random_genomes(self.n_random)

        return elite_genomes + bred_genomes + random_genomes

    def breed_next_generation(self, fitness_results, n_genomes):
        """
        Generates a given number of genomes by breeding, through crossover and mutation, existing genomes

        :param fitness_results: a sorted list of tuples containing a fitness score in the first position and a genome in the second (returned by :func:`~holland.evolution.Evaluator.evaluate_fitness`)
        :type fitness_results: list

        :param n_genomes: the number of genomes to produce
        :type n_genomes: int


        :returns: a list of bred genomes


        :raises ValueError: if ``n_genomes < 0``

        
        .. note:: For the sake of efficiency, this method expects ``fitness_results`` to be sorted in order to properly select genomes on the basis of fitness. :func:`~holland.evolution.Evaluator.evaluate_fitness` returns sorted results.

        .. todo:: Write an example for usage


        Dependencies:
            * :func:`~holland.evolution.Selector.select_breeding_pool`
            * :func:`~holland.evolution.Selector.select_parents`
            * :func:`~holland.evolution.Crosser.cross_genomes`
            * :func:`~holland.evolution.Mutator.mutate_genome`
        """
        if n_genomes < 0:
            raise ValueError("Number of bred genomes per generation cannot be negative")

        selector = Selector(self.selection_strategy)
        crosser = Crosser(self.genome_params)
        mutator = Mutator(self.genome_params)

        next_generation = [None] * n_genomes
        breeding_pool = selector.select_breeding_pool(fitness_results)

        for i in range(n_genomes):
            parents = selector.select_parents(breeding_pool)
            offspring = crosser.cross_genomes(parents)
            mutated_offspring = mutator.mutate_genome(offspring)
            next_generation[i] = mutated_offspring

        return next_generation

    def generate_random_genomes(self, n_genomes):
        """
        Generates a given number of genomes based on genome parameters

        :param n_genomes: the number of genomes to produce
        :type n_genomes: int


        :returns: a list of randomly generated genomes


        :raises ValueError: if ``n_genomes < 0``

        .. todo:: Write an example for usage

        Dependencies:
            * :func:`~holland.utils.utils.bound_value`
        """
        if n_genomes < 0:
            raise ValueError("Number of random genomes per generation cannot be negative")

        genomes = []

        for _ in range(n_genomes):
            genome = {}
            for gene_name, gene_params in self.genome_params.items():
                initial_distribution = gene_params["initial_distribution"]
                if is_list_type(gene_params):
                    if is_numeric_type(gene_params):
                        genome[gene_name] = [
                            bound_value(
                                initial_distribution(),
                                minimum=gene_params.get("min"),
                                maximum=gene_params.get("max"),
                                to_int=gene_params.get("type") == "[int]",
                            )
                            for _ in range(gene_params["size"])
                        ]
                    else:
                        genome[gene_name] = [
                            initial_distribution() for _ in range(gene_params["size"])
                        ]
                else:
                    if is_numeric_type(gene_params):
                        genome[gene_name] = bound_value(
                            initial_distribution(),
                            minimum=gene_params.get("min"),
                            maximum=gene_params.get("max"),
                            to_int=gene_params.get("type") == "int",
                        )
                    else:
                        genome[gene_name] = initial_distribution()
            genomes.append(genome)

        return genomes
