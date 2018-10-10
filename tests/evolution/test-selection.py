import numpy as np
import unittest
from unittest.mock import patch

from holland.evolution.selection import *


class SelectorInitTest(unittest.TestCase):
    def test_asserts_all_pool_parameters_are_nonnegative(self):
        """__init__ throws a ValueError if any of the given numbers in selection_strategy["pool"] is negative"""
        with self.assertRaises(ValueError):
            Selector({"pool": {"top": -1}})
        with self.assertRaises(ValueError):
            Selector({"pool": {"mid": -1}})
        with self.assertRaises(ValueError):
            Selector({"pool": {"bottom": -1}})
        with self.assertRaises(ValueError):
            Selector({"pool": {"random": -1}})

    def test_asserts_n_parents_is_at_least_1(self):
        """__init__ throws a ValueError if the given n_parents is less than 1"""
        with self.assertRaises(ValueError):
            Selector({"parents": {"n_parents": 0}})

        with self.assertRaises(ValueError):
            Selector({"parents": {"n_parents": -1}})


class SelectorSelectBreedingPoolTest(unittest.TestCase):
    def setUp(self):
        self.fitness_scores = (7, 8, 9, 10, 30, 44, 45, 50, 85, 90, 100)
        self.genomes = ("k", "j", "i", "h", "g", "f", "e", "d", "c", "b", "a")
        self.fitness_results = list(zip(self.fitness_scores, self.genomes))

    def test_asserts_top_center_bottom_and_random_sum_to_leq_population_size(self):
        """select_breeding_pool throws a ValueError if the size of the population is less than the sum of the given numbers"""
        selector = Selector({"pool": {"top": 5, "mid": 5, "bottom": 5, "random": 5}})
        with self.assertRaises(ValueError):
            selector.select_breeding_pool(self.fitness_results)

    def test_selects_correctly_with_determininstic_arguments_and_odd_population_small(
        self
    ):
        """select_breeding_pool correctly selects individuals from the top, middle, and bottom according to the given arguments when poplutation size is odd"""
        selector = Selector({"pool": {"top": 1, "mid": 1, "bottom": 1}})
        selection_pool = selector.select_breeding_pool(self.fitness_results)

        expected_selection_pool = [(100, "a"), (44, "f"), (7, "k")]
        self.assertListEqual(sorted(selection_pool), sorted(expected_selection_pool))

    def test_selects_correctly_with_determininstic_arguments_and_odd_population_larger(
        self
    ):
        """select_breeding_pool correctly selects individuals from the top, middle, and bottom according to the given arguments when poplutation size is odd"""
        selector = Selector({"pool": {"top": 3, "mid": 3, "bottom": 3}})
        selection_pool = selector.select_breeding_pool(self.fitness_results)

        expected_selection_pool = [
            (100, "a"),
            (90, "b"),
            (85, "c"),
            (45, "e"),
            (44, "f"),
            (30, "g"),
            (9, "i"),
            (8, "j"),
            (7, "k"),
        ]
        self.assertListEqual(sorted(selection_pool), sorted(expected_selection_pool))

    def test_selects_correctly_with_determininstic_arguments_and_even_population_small(
        self
    ):
        """select_breeding_pool correctly selects individuals from the top, middle, and bottom according to the given arguments when poplutation size is even"""
        fitness_results = self.fitness_results[1:]
        selector = Selector({"pool": {"top": 1, "mid": 1, "bottom": 1}})
        selection_pool = selector.select_breeding_pool(fitness_results)

        expected_selection_pool = [(100, "a"), (45, "e"), (8, "j")]
        self.assertListEqual(sorted(selection_pool), sorted(expected_selection_pool))

    def test_selects_correctly_with_determininstic_arguments_and_even_population_larger(
        self
    ):
        """select_breeding_pool correctly selects individuals from the top, middle, and bottom according to the given arguments when poplutation size is even"""
        fitness_results = self.fitness_results[1:]
        selector = Selector({"pool": {"top": 3, "mid": 3, "bottom": 3}})
        selection_pool = selector.select_breeding_pool(fitness_results)

        expected_selection_pool = [
            (100, "a"),
            (90, "b"),
            (85, "c"),
            (50, "d"),
            (45, "e"),
            (44, "f"),
            (10, "h"),
            (9, "i"),
            (8, "j"),
        ]
        self.assertListEqual(sorted(selection_pool), sorted(expected_selection_pool))

    @patch("numpy.random.choice")
    def test_does_not_randomly_select_individuals_that_were_already_selected(
        self, mock_choice
    ):
        """narrow_selecetion_pool selects individuals randomly but does not select duplicates"""
        selector = Selector({"pool": {"top": 1, "mid": 1, "bottom": 1}})
        selector.select_breeding_pool(self.fitness_results)

        self.fitness_results.sort(key=lambda x: x[0])
        deterministic_selection_pool = [(100, "a"), (44, "f"), (7, "k")]

        used_random_id_choices = mock_choice.call_args[0][0]
        expected_random_id_choices = [
            i
            for i in range(len(self.fitness_results))
            if self.fitness_results[i] not in deterministic_selection_pool
        ]
        self.assertListEqual(used_random_id_choices, expected_random_id_choices)

    @patch("numpy.random.choice", return_value=np.array([2, 7]))
    def test_returns_selected_pool(self, mock_choice):
        """select_breeding_pool returns the fitness_results that were selected as expected"""
        selector = Selector({"pool": {"top": 2, "mid": 2, "bottom": 2, "random": 2}})
        selection_pool = selector.select_breeding_pool(self.fitness_results)

        expected_selection_pool = [
            (100, "a"),
            (90, "b"),
            (45, "e"),
            (44, "f"),
            (8, "j"),
            (7, "k"),
        ] + [self.fitness_results[i] for i in mock_choice.return_value]

        self.assertListEqual(sorted(selection_pool), sorted(expected_selection_pool))


class SelectorSelectParentsTest(unittest.TestCase):
    def setUp(self):
        self.fitness_scores = (10, 15, 5, 8)
        self.genomes = ("a", "b", "c", "d")
        self.fitness_results = list(zip(self.fitness_scores, self.genomes))
        self.selection_strategy = {
            "parents": {"weighting_function": lambda x: x * x, "n_parents": 3}
        }

    @patch("numpy.random.choice")
    def test_selects_correct_number_of_parents_according_to_weighted_fitness_scores(
        self, mock_choice
    ):
        """select_parents weights fitness_scores by the given weighting_function and samples the correct number of genomes according to these weighted fitness_scores"""
        selector = Selector(self.selection_strategy)

        selector.select_parents(self.fitness_results)

        weighting_function = self.selection_strategy["parents"]["weighting_function"]
        n_parents = self.selection_strategy["parents"]["n_parents"]
        weighted_scores = [
            weighting_function(fitness) for fitness in self.fitness_scores
        ]
        weighted_total = sum(weighted_scores)
        expected_probabilities = [
            weighted_score / weighted_total for weighted_score in weighted_scores
        ]
        mock_choice.assert_called_with(
            self.genomes, p=expected_probabilities, size=n_parents, replace=False
        )

    @patch("numpy.random.choice")
    def test_handles_negative_weighted_scores(self, mock_choice):
        """select_parents does not pass negative probabilities to np.random.choice if some weighted scores are negative"""
        self.fitness_results.append((-10, "e"))
        selection_strategy = {
            "parents": {
                **self.selection_strategy["parents"],
                "weighting_function": lambda x: x,
            }
        }
        selector = Selector(selection_strategy)

        selector.select_parents(self.fitness_results)

        actual_probabilities = mock_choice.call_args[1]["p"]
        self.assertTrue(all(p >= 0 for p in actual_probabilities))

    @patch("numpy.random.choice", return_value=["a", "b", "c"])
    def test_returns_selected_parents(self, mock_choice):
        """select_parents returns the genomes it selects"""
        selector = Selector(self.selection_strategy)
        parents = selector.select_parents(self.fitness_results)

        expected_parents = mock_choice.return_value
        self.assertListEqual(parents, expected_parents)
