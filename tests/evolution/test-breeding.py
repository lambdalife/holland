import random
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
        self.fitness_scores = (100, 90, 85, 50, 45, 44, 30, 10, 9, 8, 7)
        self.genomes = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k")
        self.fitness_results = list(zip(self.fitness_scores, self.genomes))
        self.genome_params = {"a": {"type": "float"}}
        self.selection_strategy = {
            "pool": {"top": 2, "bottom": 1, "random": 2},
            "parents": {"weighting_function": lambda x: x * x, "number": 2},
        }
        self.population_size = 50
        self.random_per_generation = 2

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
            random_per_generation=self.random_per_generation,
            population_size=self.population_size,
        )

        mock_breed.assert_called_with(
            self.fitness_results,
            self.genome_params,
            self.selection_strategy,
            self.population_size - self.random_per_generation,
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
            random_per_generation=self.random_per_generation,
        )

        mock_breed.assert_called_with(
            self.fitness_results,
            self.genome_params,
            self.selection_strategy,
            len(self.fitness_results) - self.random_per_generation,
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
            random_per_generation=self.random_per_generation,
        )

        mock_generate_random.assert_called_with(
            self.genome_params, self.random_per_generation
        )

    @patch(
        "holland.evolution.breeding.breed_next_generation",
        return_value=["a", "b", "c", "d", "e"],
    )
    @patch(
        "holland.evolution.breeding.generate_random_genomes", return_value=["f", "g"]
    )
    def test_returns_bred_and_random_individuals_in_one_list(
        self, mock_generate_random, mock_breed
    ):
        """generate_next_generation returns the results of breed_next_generation and generate_random_genomes concatenated together"""
        next_generation = generate_next_generation(
            self.fitness_results,
            self.genome_params,
            self.selection_strategy,
            random_per_generation=self.random_per_generation,
        )

        expected_next_generation = (
            mock_breed.return_value + mock_generate_random.return_value
        )
        self.assertListEqual(next_generation, expected_next_generation)


class BreedNextGenerationTest(unittest.TestCase):
    def setUp(self):
        self.fitness_scores = (100, 90, 85, 50, 45, 44, 30, 10, 9, 8, 7)
        self.genomes = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k")
        self.fitness_results = list(zip(self.fitness_scores, self.genomes))
        self.genome_params = {"a": {"type": "float"}}
        self.selection_strategy = {
            "pool": {"top": 2, "bottom": 1, "random": 2},
            "parents": {"weighting_function": lambda x: x * x, "number": 2},
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
    @patch("holland.evolution.breeding.cross")
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
    @patch("holland.evolution.breeding.cross")
    @patch("holland.evolution.breeding.mutate_genome")
    def test_calls_select_parents_correctly_with_given_number(
        self, mock_mutate, mock_cross, mock_select_parents, mock_select_pool
    ):
        """breed_next_generation selects parents according to the parents selection_strategy and random_per_generation when population_size is specified"""
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
    @patch("holland.evolution.breeding.cross")
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
    @patch("holland.evolution.breeding.cross", return_value="a")
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
    @patch("holland.evolution.breeding.cross", return_value="a")
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


class GenerateRandomIndividualsTest(unittest.TestCase):
    def setUp(self):
        self.genome_params = {
            "gene1": {
                "type": "bool",
                "size": 10,
                "initial_distribution": Mock(return_value=True),
            },
            "gene2": {
                "type": "float",
                "size": 5,
                "initial_distribution": Mock(return_value=1.5),
            },
            "gene3": {
                "type": "float",
                "size": 20,
                "initial_distribution": Mock(return_value=6.0),
                "max": 10,
                "min": 1,
            },
        }

    def test_asserts_number_is_at_least_zero(self):
        """generate_random_genomes raises a ValueError if number is less than zero"""
        with self.assertRaises(ValueError):
            generate_random_genomes(self.genome_params, -1)

    def test_returns_empty_list_if_number_is_zero(self):
        """generate_random_genomes returns an empty list if the given number is zero"""
        random_individuals = generate_random_genomes(self.genome_params, 0)

        expected_random_individuals = []
        self.assertListEqual(random_individuals, expected_random_individuals)

    def test_generates_genomes_according_to_genome_params(self):
        """generate_random_genomes generates `number` genomes with values according to each gene's initial_distribution function and with length according to size"""
        number = 10
        random_individuals = generate_random_genomes(self.genome_params, number)

        self.assertEqual(len(random_individuals), number)

        self.assertEqual(
            self.genome_params["gene1"]["initial_distribution"].call_count,
            number * self.genome_params["gene1"]["size"],
        )
        self.assertEqual(
            self.genome_params["gene2"]["initial_distribution"].call_count,
            number * self.genome_params["gene2"]["size"],
        )
        self.assertEqual(
            self.genome_params["gene3"]["initial_distribution"].call_count,
            number * self.genome_params["gene3"]["size"],
        )

        for individual in random_individuals:
            for gene_name, gene in individual.items():
                self.assertEqual(len(gene), self.genome_params[gene_name]["size"])

    @patch("holland.evolution.breeding.bound_value")
    def test_calls_bound_value_on_each_value_generated_if_type_is_float(
        self, mock_bound_value
    ):
        """generate_random_genomes calls bound_value on each value if the gene's type is float using the gene_params max and min"""
        number = 1
        generate_random_genomes(self.genome_params, number)

        expected_calls = [
            call(
                self.genome_params["gene2"]["initial_distribution"].return_value,
                minimum=None,
                maximum=None,
            )
            for _ in range(self.genome_params["gene2"]["size"])
        ] + [
            call(
                self.genome_params["gene3"]["initial_distribution"].return_value,
                minimum=self.genome_params["gene3"]["min"],
                maximum=self.genome_params["gene3"]["max"],
            )
            for _ in range(self.genome_params["gene3"]["size"])
        ]

        mock_bound_value.assert_has_calls(expected_calls)

        expected_number_of_calls = len(expected_calls)
        self.assertEqual(mock_bound_value.call_count, expected_number_of_calls)
