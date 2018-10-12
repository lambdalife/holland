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

    @patch("holland.evolution.selection.select_from")
    def test_calls_select_from_with_correct_args(self, mock_select_from):
        """select_breeding_pool calls select_from with the fitness_results and top, mid, bottom, random"""
        top = 3
        mid = 1
        bottom = 1
        random = 1
        selector = Selector({"pool": {"top": top, "mid": mid, "bottom": bottom, "random": random}})

        selector.select_breeding_pool(self.fitness_results)

        mock_select_from.assert_called_once_with(
            self.fitness_results, top=top, mid=mid, bottom=bottom, random=random
        )

    @patch("holland.evolution.selection.select_from", return_value=[(1, "a"), (2, "b")])
    def test_returns_return_value_of_select_from(self, mock_select_from):
        """select_breeding_pool returns the value it receives from select_from"""
        selector = Selector({"pool": {"top": 3, "mid": 1, "bottom": 1, "random": 1}})

        breeding_pool = selector.select_breeding_pool(self.fitness_results)

        self.assertListEqual(breeding_pool, mock_select_from.return_value)


class SelectorSelectParentsTest(unittest.TestCase):
    def setUp(self):
        self.fitness_scores = (10, 15, 5, 8)
        self.genomes = ("a", "b", "c", "d")
        self.fitness_results = list(zip(self.fitness_scores, self.genomes))
        self.selection_strategy = {
            "parents": {"weighting_function": lambda x: x * x, "n_parents": 3}
        }

    @patch("holland.evolution.selection.select_random")
    def test_selects_correct_number_of_parents_according_to_weighted_fitness_scores(
        self, mock_select_from
    ):
        """select_parents weights fitness_scores by the given weighting_function and samples the correct number of genomes according to these weighted fitness_scores"""
        selector = Selector(self.selection_strategy)

        selector.select_parents(self.fitness_results)

        weighting_function = self.selection_strategy["parents"]["weighting_function"]
        n_parents = self.selection_strategy["parents"]["n_parents"]
        weighted_scores = [weighting_function(fitness) for fitness in self.fitness_scores]
        weighted_total = sum(weighted_scores)
        expected_probabilities = [
            weighted_score / weighted_total for weighted_score in weighted_scores
        ]
        mock_select_from.assert_called_with(
            self.genomes, probabilities=expected_probabilities, n=n_parents
        )

    @patch("holland.evolution.selection.select_random")
    def test_handles_negative_weighted_scores(self, mock_select_from):
        """select_parents does not pass negative probabilities to select_random if some weighted scores are negative"""
        self.fitness_results.append((-10, "e"))
        selection_strategy = {
            "parents": {**self.selection_strategy["parents"], "weighting_function": lambda x: x}
        }
        selector = Selector(selection_strategy)

        selector.select_parents(self.fitness_results)

        actual_probabilities = mock_select_from.call_args[1]["probabilities"]
        self.assertTrue(all(p >= 0 for p in actual_probabilities))

    @patch("holland.evolution.selection.select_random", return_value=["a", "b", "c"])
    def test_returns_selected_parents(self, mock_select_from):
        """select_parents returns the genomes it selects"""
        selector = Selector(self.selection_strategy)
        parents = selector.select_parents(self.fitness_results)

        expected_parents = mock_select_from.return_value
        self.assertListEqual(parents, expected_parents)
