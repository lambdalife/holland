import math
import unittest

from holland.library.fitness_weighting_functions import *


class GetUniformWeightingFunctionTest(unittest.TestCase):
    def test_returned_function_works_as_expected(self):
        """get_uniform_weighting_function returns a function that always returns the same integer"""
        weighting_function = get_uniform_weighting_function()
        inputs = list(range(0, 100, 7))

        weighted_values = [weighting_function(i) for i in inputs]

        only_one_value = len(set(weighted_values)) == 1
        self.assertTrue(only_one_value)

        self.assertTrue(isinstance(weighted_values[0], int))


class GetLinearWeightingFunctionTest(unittest.TestCase):
    def test_returned_function_works_as_expected_with_no_params_specified(self):
        """get_linear_weighting_function returns a function that returns a linearly scaled value of its input with slope 1 if slope is not specified"""
        weighting_function = get_linear_weighting_function()
        inputs = list(range(0, 100, 7))

        weighted_values = [weighting_function(i) for i in inputs]

        expected_weighted_values = inputs
        self.assertListEqual(weighted_values, expected_weighted_values)

    def test_returned_function_works_as_expected_with_slope_specified(self):
        """get_linear_weighting_function returns a function that returns a linearly scaled value of its input with slope as specified"""
        slope = 3.5
        weighting_function = get_linear_weighting_function(slope=slope)
        inputs = list(range(0, 100, 7))

        weighted_values = [weighting_function(i) for i in inputs]

        expected_weighted_values = [i * slope for i in inputs]
        self.assertListEqual(weighted_values, expected_weighted_values)


class GetPolynomialWeightingFunctionTest(unittest.TestCase):
    def test_returned_function_works_as_expected_with_no_params_specified(self):
        """get_polynomial_weighting_function returns a function that returns the input squared if power is not specified"""
        weighting_function = get_polynomial_weighting_function()
        inputs = list(range(0, 100, 7))

        weighted_values = [weighting_function(i) for i in inputs]

        expected_weighted_values = [i * i for i in inputs]
        self.assertListEqual(weighted_values, expected_weighted_values)

    def test_returned_function_works_as_expected_with_slope_specified(self):
        """get_polynomial_weighting_function returns a function that returns the input raised to the power specified"""
        power = 3.5
        weighting_function = get_polynomial_weighting_function(power=power)
        inputs = list(range(0, 100, 7))

        weighted_values = [weighting_function(i) for i in inputs]

        expected_weighted_values = [i ** power for i in inputs]
        self.assertListEqual(weighted_values, expected_weighted_values)


class GetExponentialWeightingFunctionTest(unittest.TestCase):
    def test_returned_function_works_as_expected_with_no_params_specified(self):
        """get_exponential_weighting_function returns a function that returns e raised to the input power if base is not specified"""
        weighting_function = get_exponential_weighting_function()
        inputs = list(range(0, 100, 7))

        weighted_values = [weighting_function(i) for i in inputs]

        expected_base = math.e
        expected_weighted_values = [expected_base ** i for i in inputs]
        self.assertListEqual(weighted_values, expected_weighted_values)

    def test_returned_function_works_as_expected_with_slope_specified(self):
        """get_exponential_weighting_function returns a function that returns base raised to the input power if base is specified"""
        base = 3.5
        weighting_function = get_exponential_weighting_function(base=base)
        inputs = list(range(0, 100, 7))

        weighted_values = [weighting_function(i) for i in inputs]

        expected_weighted_values = [base ** i for i in inputs]
        self.assertListEqual(weighted_values, expected_weighted_values)


class GetLogarithmicWeightingFunctionTest(unittest.TestCase):
    def test_returned_function_works_as_expected_with_no_params_specified(self):
        """get_logarithmic_weighting_function returns a function that returns the natural logarithm (base e) of the input if no base is specified"""
        weighting_function = get_logarithmic_weighting_function()
        inputs = list(range(1, 100, 7))

        weighted_values = [weighting_function(i) for i in inputs]

        expected_base = math.e
        expected_weighted_values = [math.log(i, expected_base) for i in inputs]
        self.assertListEqual(weighted_values, expected_weighted_values)

    def test_returned_function_works_as_expected_with_slope_specified(self):
        """get_logarithmic_weighting_function returns a function that returns the logarithm of the input with the specified base"""
        base = 3.5
        weighting_function = get_logarithmic_weighting_function(base=base)
        inputs = list(range(1, 100, 7))

        weighted_values = [weighting_function(i) for i in inputs]

        expected_weighted_values = [math.log(i, base) for i in inputs]
        self.assertListEqual(weighted_values, expected_weighted_values)


class GetReciprocalWeightingFunctionTest(unittest.TestCase):
    def test_returned_function_works_as_expected(self):
        """get_reciprocal_weighting_function returns a function that returns 1/input when given input"""
        weighting_function = get_reciprocal_weighting_function()
        inputs = list(range(1, 100, 7))

        weighted_values = [weighting_function(i) for i in inputs]

        expected_weighted_values = [1 / i for i in inputs]
        self.assertListEqual(weighted_values, expected_weighted_values)
