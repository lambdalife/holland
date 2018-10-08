import numpy as np
import unittest
from unittest.mock import patch, call, Mock

from holland.evolution.breeding import (
    generate_next_generation,
    breed_next_generation,
    generate_random_genomes,
)


class GenerateNextGenerationTest(unittest.TestCase):
    def setUp(self):
        self.fitness_scores = (7, 8, 9, 10, 30, 44, 45, 50, 85, 90, 100)
        self.genomes = ("k", "j", "i", "h", "g", "f", "e", "d", "c", "b", "a")
        self.fitness_results = list(zip(self.fitness_scores, self.genomes))
        self.genome_params = {"a": {"type": "[float]"}}
        self.selection_strategy = {
            "pool": {"top": 2, "bottom": 1, "random": 2},
            "parents": {"weighting_function": lambda x: x * x, "n_parents": 2},
        }
        self.population_size = 50
        self.n_random = 2
        self.n_elite = 3

    def test_asserts_n_random_and_n_elites_are_nonnegative(self):
        """generate_next_generation raises a Value error if n_random or n_elite is less than zero"""
        # Random
        with self.assertRaises(ValueError):
            generate_next_generation(
                self.fitness_results,
                self.genome_params,
                self.selection_strategy,
                n_random=-1,
            )

        # Elite
        with self.assertRaises(ValueError):
            generate_next_generation(
                self.fitness_results,
                self.genome_params,
                self.selection_strategy,
                n_elite=-1,
            )

    def test_asserts_n_random_and_n_elites_sum_to_leq_population_size(self):
        """generate_next_generation raises a ValueError if n_random + n_elite > population_size"""
        n_random = 10
        n_elite = 10
        population_size = 10

        with self.assertRaises(ValueError):
            generate_next_generation(
                self.fitness_results,
                self.genome_params,
                self.selection_strategy,
                n_random=n_random,
                n_elite=n_elite,
                population_size=population_size,
            )

    @patch("holland.evolution.breeding.breed_next_generation")
    @patch("holland.evolution.breeding.generate_random_genomes")
    def test_calls_breed_next_generation_with_correct_args_if_given_popluation_size(
        self, mock_generate_random, mock_breed
    ):
        """generate_next_generation calls breed_next_generation with the correct args"""
        generate_next_generation(
            self.fitness_results,
            self.genome_params,
            self.selection_strategy,
            n_random=self.n_random,
            n_elite=self.n_elite,
            population_size=self.population_size,
        )

        mock_breed.assert_called_with(
            self.fitness_results,
            self.genome_params,
            self.selection_strategy,
            self.population_size - self.n_random - self.n_elite,
        )

    @patch("holland.evolution.breeding.breed_next_generation")
    @patch("holland.evolution.breeding.generate_random_genomes")
    def test_calls_breed_next_generation_with_correct_args_if_not_given_popluation_size(
        self, mock_generate_random, mock_breed
    ):
        """generate_next_generation calls breed_next_generation with the correct args"""
        generate_next_generation(
            self.fitness_results,
            self.genome_params,
            self.selection_strategy,
            n_random=self.n_random,
            n_elite=self.n_elite,
        )

        mock_breed.assert_called_with(
            self.fitness_results,
            self.genome_params,
            self.selection_strategy,
            len(self.fitness_results) - self.n_random - self.n_elite,
        )

    @patch("holland.evolution.breeding.breed_next_generation")
    @patch("holland.evolution.breeding.generate_random_genomes")
    def test_calls_generate_random_genomes_with_correct_args(
        self, mock_generate_random, mock_breed
    ):
        """generate_next_generation calls generate_random_genomes with the correct args"""
        generate_next_generation(
            self.fitness_results,
            self.genome_params,
            self.selection_strategy,
            n_random=self.n_random,
        )

        mock_generate_random.assert_called_with(self.genome_params, self.n_random)

    @patch(
        "holland.evolution.breeding.breed_next_generation",
        return_value=["v", "w", "x", "y", "z"],
    )
    @patch(
        "holland.evolution.breeding.generate_random_genomes", return_value=["t", "u"]
    )
    def test_returns_bred_and_random_individuals_in_one_list(
        self, mock_generate_random, mock_breed
    ):
        """generate_next_generation returns the results of breed_next_generation and generate_random_genomes concatenated together"""
        next_generation = generate_next_generation(
            self.fitness_results,
            self.genome_params,
            self.selection_strategy,
            n_random=self.n_random,
        )

        expected_next_generation = (
            mock_breed.return_value + mock_generate_random.return_value
        )
        self.assertListEqual(sorted(next_generation), sorted(expected_next_generation))

    @patch(
        "holland.evolution.breeding.breed_next_generation",
        return_value=["v", "w", "x", "y", "z"],
    )
    @patch(
        "holland.evolution.breeding.generate_random_genomes", return_value=["t", "u"]
    )
    def test_returns_bred_random_and_elite_individuals_in_one_list(
        self, mock_generate_random, mock_breed
    ):
        """generate_next_generation returns the results of breed_next_generation and generate_random_genomes and the top n_elite individuals from the current generation all concatenated together"""
        next_generation = generate_next_generation(
            self.fitness_results,
            self.genome_params,
            self.selection_strategy,
            n_random=self.n_random,
            n_elite=self.n_elite,
        )

        elites = [g for s, g in self.fitness_results[-self.n_elite :]]
        expected_next_generation = (
            elites + mock_breed.return_value + mock_generate_random.return_value
        )
        self.assertListEqual(sorted(next_generation), sorted(expected_next_generation))


class BreedNextGenerationTest(unittest.TestCase):
    def setUp(self):
        self.fitness_scores = (100, 90, 85, 50, 45, 44, 30, 10, 9, 8, 7)
        self.genomes = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k")
        self.fitness_results = list(zip(self.fitness_scores, self.genomes))
        self.genome_params = {"a": {"type": "[float]"}}
        self.selection_strategy = {
            "pool": {"top": 2, "bottom": 1, "random": 2},
            "parents": {"weighting_function": lambda x: x * x, "n_parents": 2},
        }
        self.number = 10

    def test_asserts_number_is_at_least_zero(self):
        """breed_next_generation raises a ValueError if the given number is negative"""
        with self.assertRaises(ValueError):
            breed_next_generation(
                self.fitness_results, self.genome_params, self.selection_strategy, -1
            )

    def test_returns_empty_list_if_number_is_zero(self):
        """breed_next_generation returns an empty list if the given number is zero"""
        bred_individuals = breed_next_generation(
            self.fitness_results, self.genome_params, self.selection_strategy, 0
        )

        expected_bred_individuals = []
        self.assertListEqual(bred_individuals, expected_bred_individuals)

    @patch("holland.evolution.breeding.select_breeding_pool")
    @patch("holland.evolution.breeding.select_parents")
    @patch("holland.evolution.breeding.cross_genomes")
    @patch("holland.evolution.breeding.mutate_genome")
    def test_calls_select_breeding_pool_correctly(
        self, mock_mutate, mock_cross, mock_select_parents, mock_select_pool
    ):
        """breed_next_generation selects a breeding pool using the fitness results of the current generation"""
        breed_next_generation(
            self.fitness_results,
            self.genome_params,
            self.selection_strategy,
            self.number,
        )

        mock_select_pool.assert_called_with(
            self.fitness_results, **self.selection_strategy["pool"]
        )

    @patch(
        "holland.evolution.breeding.select_breeding_pool",
        return_value=[(100, "a"), (90, "b")],
    )
    @patch("holland.evolution.breeding.select_parents")
    @patch("holland.evolution.breeding.cross_genomes")
    @patch("holland.evolution.breeding.mutate_genome")
    def test_calls_select_parents_correctly_with_given_number(
        self, mock_mutate, mock_cross, mock_select_parents, mock_select_pool
    ):
        """breed_next_generation selects parents according to the parents selection_strategy and n_random when population_size is specified"""
        breed_next_generation(
            self.fitness_results,
            self.genome_params,
            self.selection_strategy,
            self.number,
        )

        expected_number_of_calls = self.number
        expected_calls = [
            call(mock_select_pool.return_value, **self.selection_strategy["parents"])
            for _ in range(expected_number_of_calls)
        ]
        mock_select_parents.assert_has_calls(expected_calls)
        self.assertEqual(mock_select_parents.call_count, expected_number_of_calls)

    @patch(
        "holland.evolution.breeding.select_breeding_pool",
        return_value=[(100, "a"), (90, "b")],
    )
    @patch("holland.evolution.breeding.select_parents", return_value=["a", "b"])
    @patch("holland.evolution.breeding.cross_genomes")
    @patch("holland.evolution.breeding.mutate_genome")
    def test_calls_cross_correctly(
        self, mock_mutate, mock_cross, mock_select_parents, mock_select_pool
    ):
        """breed_next_generation crosses the genomes of the parents to create an offspring genome"""
        breed_next_generation(
            self.fitness_results,
            self.genome_params,
            self.selection_strategy,
            self.number,
        )

        expected_calls = [
            call(mock_select_parents.return_value, self.genome_params)
            for _ in range(self.number)
        ]
        mock_cross.assert_has_calls(expected_calls)

    @patch(
        "holland.evolution.breeding.select_breeding_pool",
        return_value=[(100, "a"), (90, "b")],
    )
    @patch("holland.evolution.breeding.select_parents", return_value=["a", "b"])
    @patch("holland.evolution.breeding.cross_genomes", return_value="a")
    @patch("holland.evolution.breeding.mutate_genome")
    def test_calls_mutate_genome_on_offspring(
        self, mock_mutate, mock_cross, mock_select_parents, mock_select_pool
    ):
        """breed_next_generation mutates the genome of the offspring created"""
        breed_next_generation(
            self.fitness_results,
            self.genome_params,
            self.selection_strategy,
            self.number,
        )

        expected_calls = [
            call(mock_cross.return_value, self.genome_params)
            for _ in range(self.number)
        ]
        mock_mutate.assert_has_calls(expected_calls)

    @patch(
        "holland.evolution.breeding.select_breeding_pool",
        return_value=[(100, "a"), (90, "b")],
    )
    @patch("holland.evolution.breeding.select_parents", return_value=["a", "b"])
    @patch("holland.evolution.breeding.cross_genomes", return_value="a")
    @patch("holland.evolution.breeding.mutate_genome")
    def test_returns_the_next_population(
        self, mock_mutate, mock_cross, mock_select_parents, mock_select_pool
    ):
        """breed_next_generation returns the list of the mutated_offspring generated"""
        mutated_genomes = ["a", "b", "c", "d", "e"]
        mock_mutate.side_effect = mutated_genomes

        next_generation = breed_next_generation(
            self.fitness_results,
            self.genome_params,
            self.selection_strategy,
            len(mutated_genomes),
        )

        expected_next_generation = mutated_genomes
        self.assertListEqual(next_generation, expected_next_generation)


class GenerateRandomGenomesTest(unittest.TestCase):
    def setUp(self):
        self.list_genome_params = {
            "gene1": {
                "type": "[bool]",
                "size": 10,
                "initial_distribution": Mock(return_value=True),
            },
            "gene2": {
                "type": "[float]",
                "size": 5,
                "initial_distribution": Mock(return_value=1.5),
            },
            "gene3": {
                "type": "[int]",
                "size": 20,
                "initial_distribution": Mock(return_value=6),
                "max": 10,
                "min": 1,
            },
        }

        self.value_genome_params = {
            "gene1": {"type": "bool", "initial_distribution": Mock(return_value=True)},
            "gene2": {"type": "float", "initial_distribution": Mock(return_value=1.5)},
            "gene3": {
                "type": "int",
                "initial_distribution": Mock(return_value=6),
                "max": 10,
                "min": 1,
            },
        }

    def test_asserts_number_is_at_least_zero(self):
        """generate_random_genomes raises a ValueError if number is less than zero"""
        with self.assertRaises(ValueError):
            generate_random_genomes(self.list_genome_params, -1)

    def test_returns_empty_list_if_number_is_zero(self):
        """generate_random_genomes returns an empty list if the given number is zero"""
        random_genomes = generate_random_genomes(self.list_genome_params, 0)

        expected_random_individuals = []
        self.assertListEqual(random_genomes, expected_random_individuals)

    def test_generates_genomes_according_to_genome_params_for_list_type_genes(self):
        """generate_random_genomes generates `number` genomes with values according to each gene's initial_distribution function and with length according to size"""
        number = 10

        random_genomes = generate_random_genomes(self.list_genome_params, number)

        self.assertEqual(len(random_genomes), number)

        for gene_name, gene_params in self.list_genome_params.items():
            self.assertEqual(
                gene_params["initial_distribution"].call_count,
                number * gene_params["size"],
            )

        for genome in random_genomes:
            for gene_name, gene in genome.items():
                self.assertEqual(len(gene), self.list_genome_params[gene_name]["size"])

    def test_generates_genomes_according_to_genome_params_for_value_type_genes(self):
        """generate_random_genomes generates `number` genomes with values according to each gene's initial_distribution function"""
        number = 10
        random_genomes = generate_random_genomes(self.value_genome_params, number)

        self.assertEqual(len(random_genomes), number)

        for gene_name, gene_params in self.value_genome_params.items():
            self.assertEqual(gene_params["initial_distribution"].call_count, number)

        for genome in random_genomes:
            for gene_name, gene in genome.items():
                self.assertFalse(isinstance(gene, list))

    @patch("holland.evolution.breeding.bound_value")
    def test_calls_bound_value_on_each_value_generated_if_type_is_list_numeric(
        self, mock_bound_value
    ):
        """generate_random_genomes calls bound_value on each value if the gene's type is numeric using the gene_params max and min"""
        number = 1

        generate_random_genomes(self.list_genome_params, number)

        expected_calls = [
            call(
                self.list_genome_params["gene2"]["initial_distribution"].return_value,
                minimum=self.list_genome_params["gene2"].get("min"),
                maximum=self.list_genome_params["gene2"].get("max"),
                to_int=False,
            )
            for _ in range(self.list_genome_params["gene2"]["size"])
        ] + [
            call(
                self.list_genome_params["gene3"]["initial_distribution"].return_value,
                minimum=self.list_genome_params["gene3"]["min"],
                maximum=self.list_genome_params["gene3"]["max"],
                to_int=True,
            )
            for _ in range(self.list_genome_params["gene3"]["size"])
        ]

        mock_bound_value.assert_has_calls(expected_calls)

        expected_number_of_calls = len(expected_calls)
        self.assertEqual(mock_bound_value.call_count, expected_number_of_calls)

    @patch("holland.evolution.breeding.bound_value")
    def test_calls_bound_value_on_the_generated_value_if_type_is_numeric(
        self, mock_bound_value
    ):
        """generate_random_genomes calls bound_value on the output of initial_distribution if type is numeric"""
        number = 1

        generate_random_genomes(self.value_genome_params, number)

        expected_calls = [
            call(
                self.value_genome_params["gene2"]["initial_distribution"].return_value,
                minimum=self.list_genome_params["gene2"].get("min"),
                maximum=self.list_genome_params["gene2"].get("max"),
                to_int=False,
            ),
            call(
                self.value_genome_params["gene3"]["initial_distribution"].return_value,
                minimum=self.list_genome_params["gene3"]["min"],
                maximum=self.list_genome_params["gene3"]["max"],
                to_int=True,
            ),
        ]

        mock_bound_value.assert_has_calls(expected_calls)

        expected_number_of_calls = 2
        self.assertEqual(mock_bound_value.call_count, expected_number_of_calls)

    def test_does_not_return_floats_for_type_int(self):
        """generate_random_genomes returns a list of ints or an individual int if type is int or [int] and no floats"""
        number = 1
        genome_params = {
            "gene1": {
                "type": "int",
                "min": 2.5,
                "max": 10.5,
                "initial_distribution": lambda: 45.2,
            },
            "gene2": {
                "type": "int",
                "min": 2.5,
                "max": 10.5,
                "initial_distribution": lambda: 4.6,
            },
            "gene3": {
                "type": "[int]",
                "size": 5,
                "min": 2.5,
                "max": 10.5,
                "initial_distribution": lambda: -45.2,
            },
            "gene4": {
                "type": "[int]",
                "size": 5,
                "min": 2.5,
                "max": 10.5,
                "initial_distribution": lambda: 4.6,
            },
        }

        random_genomes = generate_random_genomes(genome_params, number)

        # value-types
        self.assertTrue(isinstance(random_genomes[0]["gene1"], int))
        self.assertTrue(isinstance(random_genomes[0]["gene2"], int))
        # list-types
        self.assertTrue(all(isinstance(x, int) for x in random_genomes[0]["gene3"]))
        self.assertTrue(all(isinstance(x, int) for x in random_genomes[0]["gene3"]))
