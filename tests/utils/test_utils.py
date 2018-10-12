import math
import random
import unittest
from unittest.mock import patch

from holland.utils.utils import *


class BoundValueTest(unittest.TestCase):
    def setUp(self):
        self.minimum = 0
        self.maximum = 10

    def test_returns_minimum_if_value_is_less_than_minimum(self):
        """bound_value returns the minimum if the value is less than the minimum"""
        value = self.minimum - 10

        output = bound_value(value, minimum=self.minimum, maximum=self.maximum)

        self.assertEqual(output, self.minimum)

    def test_returns_maximum_if_value_is_greater_than_maximum(self):
        """bound_value returns the maximum if the value is greater than the maximum"""
        value = self.maximum + 10

        output = bound_value(value, minimum=self.minimum, maximum=self.maximum)

        self.assertEqual(output, self.maximum)

    def test_returns_value_if_value_is_between_min_and_max(self):
        """bound_value returns the value if that value is between the given minimum and maximum"""
        value = (self.maximum - self.minimum) / 2 + self.minimum

        output = bound_value(value, minimum=self.minimum, maximum=self.maximum)

        self.assertEqual(output, value)

    @patch("holland.utils.utils.max")
    @patch("holland.utils.utils.min")
    def test_uses_inf_and_negative_inf_as_defaults(self, mock_min, mock_max):
        """bound_value uses -inf as default for minimum and inf as default for maximum"""
        value = 5

        # No min
        bound_value(value, maximum=self.maximum)
        mock_max.asset_called_with(value, -math.inf)
        mock_min.assert_called_with(mock_max.return_value, self.maximum)

        mock_max.reset_mock()
        mock_min.reset_mock()

        # No max
        bound_value(value, minimum=self.minimum)
        mock_max.assert_called_with(value, self.minimum)
        mock_min.assert_called_with(mock_max.return_value, math.inf)

        mock_max.reset_mock()
        mock_min.reset_mock()

        # Neither
        bound_value(value)
        mock_max.assert_called_with(value, -math.inf)
        mock_min.assert_called_with(mock_max.return_value, math.inf)

    @patch("holland.utils.utils.max")
    @patch("holland.utils.utils.min")
    def test_replaces_None_with_inf_or_negative_inf(self, mock_min, mock_max):
        """bound_value repalces None with -inf for minimum and inf for maximum"""
        value = 5

        # Min is None
        bound_value(value, minimum=None, maximum=self.maximum)
        mock_max.asset_called_with(value, -math.inf)
        mock_min.assert_called_with(mock_max.return_value, self.maximum)

        mock_max.reset_mock()
        mock_min.reset_mock()

        # Max is None
        bound_value(value, minimum=self.minimum, maximum=None)
        mock_max.assert_called_with(value, self.minimum)
        mock_min.assert_called_with(mock_max.return_value, math.inf)

        mock_max.reset_mock()
        mock_min.reset_mock()

        # Both are None
        bound_value(value, minimum=None, maximum=None)
        mock_max.assert_called_with(value, -math.inf)
        mock_min.assert_called_with(mock_max.return_value, math.inf)

    def test_returns_int_if_to_int_is_True(self):
        """bound_value returns an int if to_int is True"""
        for maximum in [15, 9.4]:
            value = 10.5
            minimum = 2

            output = bound_value(value, minimum=minimum, maximum=maximum, to_int=True)

            self.assertTrue(isinstance(output, int))

    def test_does_not_cast_to_int_if_to_int_is_False(self):
        """bound_value does not cast to int if to_int is False"""
        value = 10.5
        minimum = 2
        maximum = 15

        output = bound_value(value, minimum=minimum, maximum=maximum, to_int=False)

        self.assertFalse(isinstance(output, int))

    def test_returns_an_int_above_the_minimum_if_minimum_is_float_and_to_int(self):
        """bound_value returns the closest int above the minimum if minimum has a decimal and to_int is True and value < minimum or value < ceil(minimum)"""
        for value in [1, 2.7]:
            minimum = 2.3
            maximum = 15

            output = bound_value(value, minimum=minimum, maximum=maximum, to_int=True)

            expected_output = 3
            self.assertEqual(output, expected_output)


class SelectFromTest(unittest.TestCase):
    def setUp(self):
        self.values = [7, 8, 9, 10, 30, 44, 45, 50, 85, 90, 100]

    def test_asserts_top_center_bottom_and_random_sum_to_leq_num_values(self):
        """select_from throws a ValueError if the sum of the given numbers is greater than the number of values"""
        with self.assertRaises(ValueError):
            select_from(self.values, top=5, mid=5, bottom=5, random=5)

    def test_asserts_all_given_parameters_are_nonnegative(self):
        """select_from throws a ValueError if any of the given numbers is negative"""
        with self.assertRaises(ValueError):
            select_from(self.values, top=-1)
        with self.assertRaises(ValueError):
            select_from(self.values, mid=-1)
        with self.assertRaises(ValueError):
            select_from(self.values, bottom=-1)
        with self.assertRaises(ValueError):
            select_from(self.values, random=-1)

    def test_selects_correctly_with_determininstic_arguments_and_odd_population_small(self):
        """select_from correctly selects values from the top, middle, and bottom according to the given arguments when length of values is odd"""
        selection_pool = select_from(self.values, top=1, mid=1, bottom=1)

        expected_selected_values = [100, 44, 7]
        self.assertListEqual(sorted(selection_pool), sorted(expected_selected_values))

    def test_selects_correctly_with_determininstic_arguments_and_odd_num_values_larger(self):
        """select_from correctly selects values from the top, middle, and bottom according to the given arguments when length of values is odd"""
        selection_pool = select_from(self.values, top=3, mid=3, bottom=3)

        expected_selected_values = [100, 90, 85, 45, 44, 30, 9, 8, 7]
        self.assertListEqual(sorted(selection_pool), sorted(expected_selected_values))

    def test_selects_correctly_with_determininstic_arguments_and_even_num_values_small(self):
        """select_from correctly selects values from the top, middle, and bottom according to the given arguments when length of values is even"""
        values = self.values[1:]
        selection_pool = select_from(values, top=1, mid=1, bottom=1)

        expected_selected_values = [100, 45, 8]
        self.assertListEqual(sorted(selection_pool), sorted(expected_selected_values))

    def test_selects_correctly_with_determininstic_arguments_and_even_num_values_larger(self):
        """select_from correctly selects values from the top, middle, and bottom according to the given arguments when length of values is even"""
        values = self.values[1:]
        selection_pool = select_from(values, top=3, mid=3, bottom=3)

        expected_selected_values = [100, 90, 85, 50, 45, 44, 10, 9, 8]
        self.assertListEqual(sorted(selection_pool), sorted(expected_selected_values))

    @patch("holland.utils.utils.select_random")
    def test_does_not_randomly_select_values_that_were_already_selected(self, mock_select_random):
        """select_from selects values randomly but does not select duplicates"""
        select_from(self.values, top=1, mid=1, bottom=1)

        deterministic_selection_pool = [100, 44, 7]

        used_random_choices = mock_select_random.call_args[0][0]
        expected_random_choices = [
            value for value in self.values if value not in deterministic_selection_pool
        ]
        self.assertListEqual(used_random_choices, expected_random_choices)

    @patch("holland.utils.utils.select_random", return_value=[1000, 2000])
    def test_returns_selected_pool(self, mock_select_random):
        """select_from returns the values that were selected as expected"""
        selection_pool = select_from(self.values, top=2, mid=2, bottom=2, random=2)

        expected_selected_values = [100, 90, 45, 44, 8, 7] + mock_select_random.return_value

        self.assertListEqual(sorted(selection_pool), sorted(expected_selected_values))


class SelectRandomTest(unittest.TestCase):
    def test_asserts_choices_and_probabilities_match(self):
        """select_random throws a ValueError if probabilities is given but len(probabilites) != len(choices)"""
        choices = [1, 2, 3]
        probabilities = [0.5, 0.5]

        with self.assertRaises(ValueError):
            select_random(choices, probabilities=probabilities)

    def test_asserts_n_leq_len_choices_if_should_not_replace(self):
        """select_random throws a ValueError if should_replace is False but n > len(choices)"""
        choices = [1, 2, 3]
        n = len(choices) + 1

        with self.assertRaises(ValueError):
            select_random(choices, n=n, should_replace=False)

    def test_asserts_probabilities_are_nonnegative(self):
        """select_random throws a ValueError if any element of probabilities is negative"""
        choices = [1, 2, 3]
        probabilities = [0.75, 0.75, -0.5]

        with self.assertRaises(ValueError):
            select_random(choices, probabilities=probabilities)

    def test_asserts_probabilities_are_normalized(self):
        """select_random throws a ValueError if the sum of the given probabilities is not 1"""
        choices = [1, 2, 3]

        # less than 1
        with self.assertRaises(ValueError):
            probabilities = [0.1, 0.1, 0.1]
            select_random(choices, probabilities=probabilities)

        # greater than 1
        with self.assertRaises(ValueError):
            probabilities = [1, 1, 1]
            select_random(choices, probabilities=probabilities)

    def test_returns_a_list_of_length_n(self):
        """select_random returns a list of size n"""
        choices = list(range(10))

        for n in range(10):
            selected = select_random(choices, n=n)
            self.assertEqual(len(selected), n)

    def test_no_duplicates_if_should_not_replace(self):
        """select_random returns a list that contains no duplicates if should_replace is False"""
        choices = list(range(10))
        n = 5

        for _ in range(100):  # 100 times because it could randomly pass
            selected = select_random(choices, n=n)
            self.assertEqual(len(selected), len(set(selected)))

    def test_selects_elements_according_to_respective_probabilities(self):
        """select_random selects elements according to the given probabilities"""
        choices = list(range(10))
        n = 1
        probabilities = [1] + ([0] * (len(choices) - 1))

        selected = select_random(choices, probabilities=probabilities, n=n)

        expected_selected = [choices[0]]
        self.assertListEqual(selected, expected_selected)

    def test_handles_nested_structures(self):
        """select_random does not throw an error if the elements of choices are lists, dicts, or tuples"""
        choices = [[1], [2], [3]]
        selected = select_random(choices)
        self.assertTrue(isinstance(selected[0], list))

        choices = [{"a": 1}, {"b": 2}, {"c": 3}]
        selected = select_random(choices)
        self.assertTrue(isinstance(selected[0], dict))

        choices = [(1,), (2,), (3,)]
        selected = select_random(choices)
        self.assertTrue(isinstance(selected[0], tuple))


class IsNumericTypeTest(unittest.TestCase):
    def test_returns_False_if_is_not_numeric_type(self):
        """is_numeric_type returns False if the type is not int or float"""
        self.assertFalse(is_numeric_type({"type": "bool"}))
        self.assertFalse(is_numeric_type({"type": "[bool]"}))
        self.assertFalse(is_numeric_type({"type": "str"}))
        self.assertFalse(is_numeric_type({"type": "[str]"}))

    def test_returns_True_if_is_numeric_type(self):
        """is_numeric_type returns True if the type is int or float"""
        self.assertTrue(is_numeric_type({"type": "int"}))
        self.assertTrue(is_numeric_type({"type": "[int]"}))
        self.assertTrue(is_numeric_type({"type": "float"}))
        self.assertTrue(is_numeric_type({"type": "[float]"}))


class IsListTypeTest(unittest.TestCase):
    def test_returns_False_if_is_not_list_type(self):
        """is_list_type returns False if the type is not wrapped in brackets"""
        self.assertFalse(is_list_type({"type": "bool"}))
        self.assertFalse(is_list_type({"type": "float"}))
        self.assertFalse(is_list_type({"type": "int"}))
        self.assertFalse(is_list_type({"type": "str"}))

    def test_returns_True_if_is_list_type(self):
        """is_list_type returns True if the type is wrapped in brackets"""
        self.assertTrue(is_list_type({"type": "[bool]"}))
        self.assertTrue(is_list_type({"type": "[float]"}))
        self.assertTrue(is_list_type({"type": "[int]"}))
        self.assertTrue(is_list_type({"type": "[str]"}))
