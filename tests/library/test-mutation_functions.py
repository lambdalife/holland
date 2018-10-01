import unittest
from unittest.mock import patch

from holland.library.mutation_functions import (
    get_flip_mutator,
    get_boundary_mutator,
    get_uniform_mutator,
    get_gaussian_mutator,
)


class GetFlipMutatorTest(unittest.TestCase):
    def test_returned_function_works_as_expected_when_given_True(self):
        """get_flip_mutator returns a function that returns False when given True"""
        flip_mutate = get_flip_mutator()
        value = True
        result = flip_mutate(value)
        self.assertFalse(result)

    def test_returned_function_works_as_expected_when_given_False(self):
        """get_flip_mutator returns a function that returns True when given False"""
        flip_mutate = get_flip_mutator()
        value = False
        result = flip_mutate(value)
        self.assertTrue(result)


class GetBoundaryMutatorTest(unittest.TestCase):
    def test_returned_function_works_as_expected(self):
        """get_boundary_mutator returns a function that randomly returns either the minimum or maximum specified"""
        minimum = 0
        maximum = 100
        boundary_mutate = get_boundary_mutator(minimum, maximum)
        value = 50

        with patch("random.random", return_value=0.1):
            output = boundary_mutate(value)
            expected_output = minimum
            self.assertEqual(output, expected_output)

        with patch("random.random", return_value=0.9):
            output = boundary_mutate(value)
            expected_output = maximum
            self.assertEqual(output, expected_output)


class GetUniformMutatorTest(unittest.TestCase):
    @patch("random.uniform", return_value=26.4)
    def test_returned_function_works_as_expected(self, mock_uniform):
        """get_uniform_mutator returns a function that randomly selects a value between the given minimum and maximum"""
        minimum = 0
        maximum = 100
        uniform_mutate = get_uniform_mutator(minimum, maximum)
        value = 50

        output = uniform_mutate(value)

        expected_output = mock_uniform.return_value
        self.assertEqual(output, expected_output)
        mock_uniform.assert_called_with(minimum, maximum)


class GetGaussianMutatorTest(unittest.TestCase):
    @patch("random.gauss", return_value=40.5)
    def test_returned_function_works_as_expected(self, mock_gauss):
        """get_gaussian_mutator returns a function that randomly selects a value from a gaussian distribution with mu=value sigma=sigma"""
        sigma = 10
        gaussian_mutate = get_gaussian_mutator(sigma)
        value = 50

        output = gaussian_mutate(value)

        expected_output = mock_gauss.return_value
        self.assertEqual(output, expected_output)
        mock_gauss.assert_called_with(value, sigma)
