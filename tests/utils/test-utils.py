import numpy as np
import unittest
from unittest.mock import patch

from holland.utils.utils import bound_value


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
