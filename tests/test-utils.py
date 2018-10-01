import unittest

from holland.utils import bound_value


class BoundValueTest(unittest.TestCase):
    def setUp(self):
        self.minimum = 0
        self.maximum = 10

    def test_returns_minimum_if_value_is_less_than_minimum(self):
        """bound_value returns the minimum if the value is less than the minimum"""
        value = self.minimum - 10

        output = bound_value(value, self.minimum, self.maximum)

        self.assertEqual(output, self.minimum)

    def test_returns_maximum_if_value_is_greater_than_maximum(self):
        """bound_value returns the maximum if the value is greater than the maximum"""
        value = self.maximum + 10

        output = bound_value(value, self.minimum, self.maximum)

        self.assertEqual(output, self.maximum)

    def test_returns_value_if_value_is_between_min_and_max(self):
        """bound_value returns the value if that value is between the given minimum and maximum"""
        value = (self.maximum - self.minimum) / 2 + self.minimum

        output = bound_value(value, self.minimum, self.maximum)

        self.assertEqual(output, value)
