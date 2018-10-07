import numpy as np
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
        """bound_value uses -np.inf as default for minimum and np.inf as default for maximum"""
        value = 5

        # No min
        bound_value(value, maximum=self.maximum)
        mock_max.asset_called_with(value, -np.inf)
        mock_min.assert_called_with(mock_max.return_value, self.maximum)

        mock_max.reset_mock()
        mock_min.reset_mock()

        # No max
        bound_value(value, minimum=self.minimum)
        mock_max.assert_called_with(value, self.minimum)
        mock_min.assert_called_with(mock_max.return_value, np.inf)

        # Neither
        bound_value(value)
        mock_max.assert_called_with(value, -np.inf)
        mock_min.assert_called_with(mock_max.return_value, np.inf)

    @patch("holland.utils.utils.max")
    @patch("holland.utils.utils.min")
    def test_replaces_None_with_inf_or_negative_inf(self, mock_min, mock_max):
        """bound_value repalces None with -np.inf for minimum and np.inf for maximum"""
        value = 5

        # Min is None
        bound_value(value, minimum=None, maximum=self.maximum)
        mock_max.asset_called_with(value, -np.inf)
        mock_min.assert_called_with(mock_max.return_value, self.maximum)

        mock_max.reset_mock()
        mock_min.reset_mock()

        # Max is None
        bound_value(value, minimum=self.minimum, maximum=None)
        mock_max.assert_called_with(value, self.minimum)
        mock_min.assert_called_with(mock_max.return_value, np.inf)

        # Both are None
        bound_value(value, minimum=None, maximum=None)
        mock_max.assert_called_with(value, -np.inf)
        mock_min.assert_called_with(mock_max.return_value, np.inf)


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

    def test_selects_correctly_with_determininstic_arguments_and_odd_population_small(
        self
    ):
        """select_from correctly selects values from the top, middle, and bottom according to the given arguments when length of values is odd"""
        selection_pool = select_from(self.values, top=1, mid=1, bottom=1)

        expected_selected_values = [100, 44, 7]
        self.assertListEqual(sorted(selection_pool), sorted(expected_selected_values))

    def test_selects_correctly_with_determininstic_arguments_and_odd_num_values_larger(
        self
    ):
        """select_from correctly selects values from the top, middle, and bottom according to the given arguments when length of values is odd"""
        selection_pool = select_from(self.values, top=3, mid=3, bottom=3)

        expected_selected_values = [100, 90, 85, 45, 44, 30, 9, 8, 7]
        self.assertListEqual(sorted(selection_pool), sorted(expected_selected_values))

    def test_selects_correctly_with_determininstic_arguments_and_even_num_values_small(
        self
    ):
        """select_from correctly selects values from the top, middle, and bottom according to the given arguments when length of values is even"""
        values = self.values[1:]
        selection_pool = select_from(values, top=1, mid=1, bottom=1)

        expected_selected_values = [100, 45, 8]
        self.assertListEqual(sorted(selection_pool), sorted(expected_selected_values))

    def test_selects_correctly_with_determininstic_arguments_and_even_num_values_larger(
        self
    ):
        """select_from correctly selects values from the top, middle, and bottom according to the given arguments when length of values is even"""
        values = self.values[1:]
        selection_pool = select_from(values, top=3, mid=3, bottom=3)

        expected_selected_values = [100, 90, 85, 50, 45, 44, 10, 9, 8]
        self.assertListEqual(sorted(selection_pool), sorted(expected_selected_values))

    @patch("numpy.random.choice")
    def test_does_not_randomly_select_values_that_were_already_selected(
        self, mock_choice
    ):
        """select_from selects values randomly but does not select duplicates"""
        select_from(self.values, top=1, mid=1, bottom=1)

        deterministic_selection_pool = [100, 44, 7]

        used_random_id_choices = mock_choice.call_args[0][0]
        expected_random_id_choices = [
            i
            for i in range(len(self.values))
            if self.values[i] not in deterministic_selection_pool
        ]
        self.assertListEqual(used_random_id_choices, expected_random_id_choices)

    @patch("numpy.random.choice", return_value=np.array([2, 7]))
    def test_returns_selected_pool(self, mock_choice):
        """select_from returns the values that were selected as expected"""
        selection_pool = select_from(self.values, top=2, mid=2, bottom=2, random=2)

        expected_selected_values = [100, 90, 45, 44, 8, 7] + [
            self.values[i] for i in mock_choice.return_value
        ]

        self.assertListEqual(sorted(selection_pool), sorted(expected_selected_values))


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
