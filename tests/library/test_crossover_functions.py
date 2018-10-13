import unittest
from unittest.mock import patch, call

from holland.library.crossover_functions import *


class GetUniformCrossoverFunctionTest(unittest.TestCase):
    @patch("random.choice")
    def test_returned_function_makes_random_choices_over_correct_options(self, mock_select_random):
        """get_uniform_crossover_function returns a function that selects each gene value randomly from each parent"""
        uniform_crossover = get_uniform_crossover_function()
        parent_genes = [list(range(1, 10)), list(range(10, 100, 10)), list(range(100, 1000, 100))]

        uniform_crossover(parent_genes)

        expected_choice_calls = [
            call((parent_genes[0][i], parent_genes[1][i], parent_genes[2][i]))
            for i in range(len(parent_genes[0]))
        ]
        mock_select_random.assert_has_calls(expected_choice_calls)
        self.assertEqual(mock_select_random.call_count, len(expected_choice_calls))

    @patch("random.choice", return_value=10)
    def test_output_of_returned_function_has_correct_length(self, mock_select_random):
        """get_uniform_crossover_function returns a function that returns a list with the same length as the parents"""
        uniform_crossover = get_uniform_crossover_function()
        parent_genes = [list(range(10)) for _ in range(5)]

        output = uniform_crossover(parent_genes)

        expected_length = len(parent_genes[0])
        self.assertEqual(len(output), expected_length)

    def test_returned_function_returns_a_single_value_if_parent_genes_are_values_not_lists(self):
        """get_uniform_crossover_function returns a function that returns a single value if the given parent_genes are each single values"""
        uniform_crossover = get_uniform_crossover_function()
        parent_genes = list(range(2))

        output = uniform_crossover(parent_genes)

        self.assertEqual(type(output), type(parent_genes[0]))


class GetPointCrossoverFunction(unittest.TestCase):
    def test_asserts_number_of_crossover_points_is_nonnegative(self):
        """get_point_crossover_function raises a ValueError if n_crossover_points is negative"""
        n_crossover_points = -1
        with self.assertRaises(ValueError):
            get_point_crossover_function(n_crossover_points=n_crossover_points)

    @patch("holland.library.crossover_functions.select_random")
    def test_selects_correct_number_of_crossover_points_from_correct_options(
        self, mock_select_random
    ):
        """get_point_crossover_function selects the correct number of crossover points from all indices of elements of parent_genes"""
        n_crossover_points = 3
        point_crossover = get_point_crossover_function(n_crossover_points=n_crossover_points)
        parent_genes = [list(range(1, 10)), list(range(10, 100, 10))]

        point_crossover(parent_genes)

        expected_point_options = range(1, len(parent_genes[0]))
        mock_select_random.assert_called_with(expected_point_options, n=n_crossover_points)

    @patch("holland.library.crossover_functions.select_random", return_value=[5])
    def test_returned_function_slices_genome_of_each_parent_with_2_parents_and_1_point(
        self, mock_select_random
    ):
        """get_point_crossover_function returns a function that picks crossover points and then slices each parent genome according to those points"""
        point_crossover = get_point_crossover_function(n_crossover_points=1)
        parent_genes = [list(range(1, 10)), list(range(10, 100, 10))]

        output = point_crossover(parent_genes)

        crossover_point = mock_select_random.return_value[0]
        expected_output = parent_genes[0][:crossover_point] + parent_genes[1][crossover_point:]
        self.assertEqual(output, expected_output)
        self.assertEqual(len(output), len(parent_genes[0]))

    @patch("holland.library.crossover_functions.select_random", return_value=[2, 5, 8])
    def test_returned_function_slices_genome_of_each_parent_with_2_parents_and_multiple_points(
        self, mock_select_random
    ):
        """get_point_crossover_function returns a function that picks crossover points and then slices each parent genome according to those points"""
        point_crossover = get_point_crossover_function(n_crossover_points=1)
        parent_genes = [list(range(1, 10)), list(range(10, 100, 10))]

        output = point_crossover(parent_genes)

        crossover_points = mock_select_random.return_value
        expected_output = (
            parent_genes[0][: crossover_points[0]]
            + parent_genes[1][crossover_points[0] : crossover_points[1]]
            + parent_genes[0][crossover_points[1] : crossover_points[2]]
            + parent_genes[1][crossover_points[2] :]
        )
        self.assertEqual(output, expected_output)
        self.assertEqual(len(output), len(parent_genes[0]))

    @patch("holland.library.crossover_functions.select_random", return_value=[2, 5, 8])
    def test_returned_function_slices_genome_of_each_parent_with_more_parents_and_multiple_points(
        self, mock_select_random
    ):
        """get_point_crossover_function returns a function that picks crossover points and then slices each parent according to those points"""
        point_crossover = get_point_crossover_function(n_crossover_points=1)
        parent_genes = [list(range(1, 10)), list(range(10, 100, 10)), list(range(100, 1000, 100))]

        output = point_crossover(parent_genes)

        crossover_points = mock_select_random.return_value
        expected_output = (
            parent_genes[0][: crossover_points[0]]
            + parent_genes[1][crossover_points[0] : crossover_points[1]]
            + parent_genes[2][crossover_points[1] : crossover_points[2]]
            + parent_genes[0][crossover_points[2] :]
        )
        self.assertEqual(output, expected_output)
        self.assertEqual(len(output), len(parent_genes[0]))


class GetAndCrossoverFunctionTest(unittest.TestCase):
    def test_returned_function_works_as_expected_with_value_type_genes(self):
        """get_and_crossover_function returns a function that returns the value of all genes 'and'ed together"""
        and_crossover = get_and_crossover_function()
        parent_genes_sets = [[True, True, True], [False, True, True], [False, False, False]]
        expected_outputs = [True, False, False]

        for parent_genes, expected_output in zip(parent_genes_sets, expected_outputs):
            output = and_crossover(parent_genes)

            self.assertEqual(output, expected_output)

    def test_returned_function_works_as_expected_with_list_type_genes(self):
        """get_and_crossover_function returns a function that returns a gene where each value is the result of 'and'ing all parent gene values at that position"""
        and_crossover = get_and_crossover_function()
        parent_genes = [[True, True, False], [True, False, False], [True, False, False]]

        output = and_crossover(parent_genes)

        expected_output = [True, False, False]
        self.assertListEqual(output, expected_output)


class GetOrCrossoverFunctionTest(unittest.TestCase):
    def test_returned_function_works_as_expected_with_value_type_genes(self):
        """get_or_crossover_function returns a function that returns the value of all genes 'or'ed together"""
        or_crossover = get_or_crossover_function()
        parent_genes_sets = [[True, True, True], [False, True, True], [False, False, False]]
        expected_outputs = [True, True, False]

        for parent_genes, expected_output in zip(parent_genes_sets, expected_outputs):
            output = or_crossover(parent_genes)

            self.assertEqual(output, expected_output)

    def test_returned_function_works_as_expected_with_list_type_genes(self):
        """get_or_crossover_function returns a function that returns a gene where each value is the result of 'or'ing all parent gene values at that position"""
        or_crossover = get_or_crossover_function()
        parent_genes = [[True, True, False], [True, False, False], [True, False, False]]

        output = or_crossover(parent_genes)

        expected_output = [True, True, False]
        self.assertListEqual(output, expected_output)
