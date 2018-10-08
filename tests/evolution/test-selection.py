import numpy as np
import unittest
from unittest.mock import patch

from holland.evolution.selection import select_breeding_pool, select_parents


class SelectBreedingPoolTest(unittest.TestCase):
    def setUp(self):
        self.fitness_scores = (7, 8, 9, 10, 30, 44, 45, 50, 85, 90, 100)
        self.genomes = ("k", "j", "i", "h", "g", "f", "e", "d", "c", "b", "a")
        self.fitness_results = list(zip(self.fitness_scores, self.genomes))

    def test_asserts_top_center_bottom_and_random_sum_to_leq_population_size(self):
        """select_breeding_pool throws a ValueError if the sum of the given numbers is greater than the size of the population"""
        with self.assertRaises(ValueError):
            select_breeding_pool(self.fitness_results, top=5, mid=5, bottom=5, random=5)

    def test_asserts_all_given_parameters_are_nonnegative(self):
        """select_breeding_pool throws a ValueError if any of the given numbers is negative"""
        with self.assertRaises(ValueError):
            select_breeding_pool(self.fitness_results, top=-1)
        with self.assertRaises(ValueError):
            select_breeding_pool(self.fitness_results, mid=-1)
        with self.assertRaises(ValueError):
            select_breeding_pool(self.fitness_results, bottom=-1)
        with self.assertRaises(ValueError):
            select_breeding_pool(self.fitness_results, random=-1)

    def test_selects_correctly_with_determininstic_arguments_and_odd_population_small(
        self
    ):
        """select_breeding_pool correctly selects individuals from the top, middle, and bottom according to the given arguments when poplutation size is odd"""
        selection_pool = select_breeding_pool(
            self.fitness_results, top=1, mid=1, bottom=1
        )

        expected_selection_pool = [(100, "a"), (44, "f"), (7, "k")]
        self.assertListEqual(sorted(selection_pool), sorted(expected_selection_pool))

    def test_selects_correctly_with_determininstic_arguments_and_odd_population_larger(
        self
    ):
        """select_breeding_pool correctly selects individuals from the top, middle, and bottom according to the given arguments when poplutation size is odd"""
        selection_pool = select_breeding_pool(
            self.fitness_results, top=3, mid=3, bottom=3
        )

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
        selection_pool = select_breeding_pool(fitness_results, top=1, mid=1, bottom=1)

        expected_selection_pool = [(100, "a"), (45, "e"), (8, "j")]
        self.assertListEqual(sorted(selection_pool), sorted(expected_selection_pool))

    def test_selects_correctly_with_determininstic_arguments_and_even_population_larger(
        self
    ):
        """select_breeding_pool correctly selects individuals from the top, middle, and bottom according to the given arguments when poplutation size is even"""
        fitness_results = self.fitness_results[1:]
        selection_pool = select_breeding_pool(fitness_results, top=3, mid=3, bottom=3)

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

        select_breeding_pool(self.fitness_results, top=1, mid=1, bottom=1)

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
        selection_pool = select_breeding_pool(
            self.fitness_results, top=2, mid=2, bottom=2, random=2
        )

        expected_selection_pool = [
            (100, "a"),
            (90, "b"),
            (45, "e"),
            (44, "f"),
            (8, "j"),
            (7, "k"),
        ] + [self.fitness_results[i] for i in mock_choice.return_value]

        self.assertListEqual(sorted(selection_pool), sorted(expected_selection_pool))


class SelectParentsTest(unittest.TestCase):
    def setUp(self):
        self.fitness_scores = (10, 15, 5, 8)
        self.genomes = ("a", "b", "c", "d")
        self.fitness_results = list(zip(self.fitness_scores, self.genomes))
        self.weighting_function = lambda x: x * x
        self.n_parents = 3

    def test_asserts_number_of_parents_is_at_least_1(self):
        """select_parents throws a ValueError if the given n_parents is less than 1"""
        with self.assertRaises(ValueError):
            select_parents(
                self.fitness_results,
                weighting_function=self.weighting_function,
                n_parents=0,
            )

        with self.assertRaises(ValueError):
            select_parents(
                self.fitness_results,
                weighting_function=self.weighting_function,
                n_parents=-1,
            )

    @patch("numpy.random.choice")
    def test_selects_correct_number_of_parents_according_to_weighted_fitness_scores(
        self, mock_choice
    ):
        """select_parents weights fitness_scores by the given weighting_function and samples the correct number of genomes according to these weighted fitness_scores"""
        select_parents(
            self.fitness_results,
            weighting_function=self.weighting_function,
            n_parents=self.n_parents,
        )

        weighted_scores = [
            self.weighting_function(fitness) for fitness in self.fitness_scores
        ]
        weighted_total = sum(weighted_scores)
        expected_probabilities = [
            weighted_score / weighted_total for weighted_score in weighted_scores
        ]
        mock_choice.assert_called_with(
            self.genomes, p=expected_probabilities, size=self.n_parents, replace=False
        )

    @patch("numpy.random.choice", return_value=["a", "b", "c"])
    def test_returns_selected_parents(self, mock_choice):
        """select_parents returns the genomes it selects"""
        parents = select_parents(
            self.fitness_results,
            weighting_function=self.weighting_function,
            n_parents=self.n_parents,
        )

        expected_parents = mock_choice.return_value
        self.assertListEqual(parents, expected_parents)
