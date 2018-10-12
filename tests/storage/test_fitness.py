import statistics
import unittest
from unittest.mock import patch

from holland.storage.fitness import record_fitness, format_fitness_statistics


class RecordFitnessTest(unittest.TestCase):
    def setUp(self):
        self.generation_num = 5
        self.fitness_scores = [1, 2, 3, 4, 5, 6]
        self.base_storage_options = {"file_name": "test", "path": "test/test"}

    @patch("holland.storage.fitness.format_fitness_statistics", return_value={"a": 1, "b": 2})
    @patch("holland.storage.fitness.record")
    def test_calls_record_with_correct_arguments(self, mock_record, mock_format):
        """record_fitness stores the formatted data to a csv if storage format is csv"""
        storage_options = {**self.base_storage_options, "format": "csv"}

        record_fitness(self.generation_num, self.fitness_scores, **storage_options)

        expected_data = mock_format.return_value
        mock_record.assert_called_with(expected_data, **storage_options)

    @patch("holland.storage.fitness.format_fitness_statistics", return_value={"a": 1, "b": 2})
    @patch("holland.storage.fitness.record")
    def test_returns_fitness_statistics(self, mock_record, mock_format):
        """record_fitness returns the fitness_statistics returned by format_fitness_statistics"""
        storage_options = {**self.base_storage_options, "format": "csv"}

        output = record_fitness(self.generation_num, self.fitness_scores, **storage_options)

        expected_output = mock_format.return_value
        self.assertDictEqual(output, expected_output)


class FormatFitnessStatisticsTest(unittest.TestCase):
    def test_formats_stats_correctly(self):
        """format_fitness_statistics returns a dictionary with keys generation, max, min, median, mean, stdev and correct values for each"""
        generation_num = 5
        fitness_scores = [1, 2, 3, 4, 5, 6]

        data = format_fitness_statistics(generation_num, fitness_scores)

        expected_data = {
            "generation": generation_num,
            "max": max(fitness_scores),
            "min": min(fitness_scores),
            "median": statistics.median(fitness_scores),
            "mean": statistics.mean(fitness_scores),
            "stdev": statistics.stdev(fitness_scores),
        }

        self.assertDictEqual(data, expected_data)
