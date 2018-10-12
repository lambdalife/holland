import unittest
from unittest.mock import patch

from holland.library.mutation_functions import (
    get_flip_mutation_function,
    get_boundary_mutation_function,
    get_uniform_mutation_function,
    get_gaussian_mutation_function,
)


class GetFlipMutationFunctionTest(unittest.TestCase):
    def test_returned_function_works_as_expected_when_given_True(self):
        """get_flip_mutation_function returns a function that returns False when given True"""
        flip_mutate = get_flip_mutation_function()
        value = True
        result = flip_mutate(value)
        self.assertFalse(result)

    def test_returned_function_works_as_expected_when_given_False(self):
        """get_flip_mutation_function returns a function that returns True when given False"""
        flip_mutate = get_flip_mutation_function()
        value = False
        result = flip_mutate(value)
        self.assertTrue(result)


class GetBoundaryMutationFunctionTest(unittest.TestCase):
    def test_returned_function_works_as_expected(self):
        """get_boundary_mutation_function returns a function that randomly returns either the minimum or maximum specified"""
        minimum = 0
        maximum = 100
        boundary_mutate = get_boundary_mutation_function(minimum, maximum)
        value = 50

        with patch("random.random", return_value=0.1):
            output = boundary_mutate(value)
            expected_output = minimum
            self.assertEqual(output, expected_output)

        with patch("random.random", return_value=0.9):
            output = boundary_mutate(value)
            expected_output = maximum
            self.assertEqual(output, expected_output)


class GetUniformMutationFunctionTest(unittest.TestCase):
    @patch("random.uniform", return_value=26.4)
    def test_returned_function_works_as_expected(self, mock_uniform):
        """get_uniform_mutation_function returns a function that randomly selects a value between the given minimum and maximum"""
        minimum = 0
        maximum = 100
        uniform_mutate = get_uniform_mutation_function(minimum, maximum)
        value = 50

        output = uniform_mutate(value)

        expected_output = mock_uniform.return_value
        self.assertEqual(output, expected_output)
        mock_uniform.assert_called_with(minimum, maximum)


class GetGaussianMutationFunctionTest(unittest.TestCase):
    @patch("random.gauss", return_value=40.5)
    def test_returned_function_works_as_expected(self, mock_gauss):
        """get_gaussian_mutation_function returns a function that randomly selects a value from a gaussian distribution with mu=value sigma=sigma"""
        sigma = 10
        gaussian_mutate = get_gaussian_mutation_function(sigma)
        value = 50

        output = gaussian_mutate(value)

        expected_output = mock_gauss.return_value
        self.assertEqual(output, expected_output)
        mock_gauss.assert_called_with(value, sigma)
