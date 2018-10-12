import random
import unittest
from unittest.mock import patch

from holland.storage.genomes_and_fitnesses import (
    record_genomes_and_fitnesses,
    format_genomes_and_fitnesses_for_storage,
)


class RecordGenomesAndFitnessesTest(unittest.TestCase):
    def setUp(self):
        pop_size = 10
        self.genomes = [{"a": [i]} for i in range(pop_size)]
        self.fitness_scores = list(range(pop_size))
        self.fitness_results = list(zip(self.fitness_scores, self.genomes))

    @patch("holland.storage.genomes_and_fitnesses.format_genomes_and_fitnesses_for_storage")
    @patch("holland.storage.genomes_and_fitnesses.record")
    def test_calls_format_genomes(self, mock_record, mock_format):
        """record_genomes_and_fitnesses calls format_genomes_and_fitnesses_for_storage with correct args"""
        generation_num = 15
        storage_options = {"file_name": "test.json"}

        record_genomes_and_fitnesses(generation_num, self.fitness_results, **storage_options)

        mock_format.assert_called_with(generation_num, self.fitness_results, **storage_options)

    @patch(
        "holland.storage.genomes_and_fitnesses.format_genomes_and_fitnesses_for_storage",
        return_value=[{"generation": 1, "genomes": [1, 2, 3]}],
    )
    @patch("holland.storage.genomes_and_fitnesses.record")
    def test_calls_record_with_correct_args_if_should_record(self, mock_record, mock_format):
        """record_genomes_and_fitnesses calls record with correct args"""
        generation_num = 15
        storage_options = {"file_name": "test.json"}

        record_genomes_and_fitnesses(generation_num, self.fitness_results, **storage_options)

        expected_data = mock_format.return_value

        mock_record.assert_called_with(expected_data, **storage_options)

    @patch("holland.storage.genomes_and_fitnesses.format_genomes_and_fitnesses_for_storage")
    @patch("holland.storage.genomes_and_fitnesses.record")
    def test_adds_generation_suffix_to_file_name_if_should_add_generation_suffix(
        self, mock_record, mock_format
    ):
        """record_genomes_and_fitnesses adds a generation_num suffix to the file_name if should_add_generation_suffix is True"""
        generation_num = 15
        storage_options = {"file_name": "test.json", "should_add_generation_suffix": True}

        record_genomes_and_fitnesses(generation_num, self.fitness_results, **storage_options)

        expected_storage_options = {**storage_options, "file_name": "test-generation_15.json"}
        mock_record.assert_called_with(mock_format.return_value, **expected_storage_options)

    @patch("holland.storage.genomes_and_fitnesses.format_genomes_and_fitnesses_for_storage")
    @patch("holland.storage.genomes_and_fitnesses.record")
    def test_adds_generation_suffix_to_file_name_correctly_when_file_has_multiple_periods(
        self, mock_record, mock_format
    ):
        """record_genomes_and_fitnesses adds a generation_num suffix to the file_name first word (separated by '.') in the file_name if should_add_generation_suffix is True"""
        generation_num = 15
        storage_options = {
            "file_name": "test.out.json",
            "record_every_n_generations": 5,
            "should_add_generation_suffix": True,
        }

        record_genomes_and_fitnesses(generation_num, self.fitness_results, **storage_options)

        expected_storage_options = {**storage_options, "file_name": "test-generation_15.out.json"}
        mock_record.assert_called_with(mock_format.return_value, **expected_storage_options)

    @patch("holland.storage.genomes_and_fitnesses.format_genomes_and_fitnesses_for_storage")
    @patch("holland.storage.genomes_and_fitnesses.record")
    def test_does_not_add_generation_suffix_to_file_name_if_not_should_add_generation_suffix(
        self, mock_record, mock_format
    ):
        """record_genomes_and_fitnesses does not add a generation_num suffix to the file_name if should_add_generation_suffix is False or not specified"""
        generation_num = 15
        storage_options_options = [
            {
                "file_name": "test.json",
                "record_every_n_generations": 5,
                "should_add_generation_suffix": False,
            },
            {"file_name": "test.json", "record_every_n_generations": 5},
        ]

        for storage_options in storage_options_options:
            record_genomes_and_fitnesses(generation_num, self.fitness_results, **storage_options)

            expected_storage_options = {**storage_options, "file_name": "test.json"}
            mock_record.assert_called_with(mock_format.return_value, **expected_storage_options)


class FormatGenomesAndFitnessesForStorage(unittest.TestCase):
    def setUp(self):
        pop_size = 10
        self.genomes = [{"a": [i]} for i in range(pop_size)]
        self.fitness_scores = list(range(pop_size))
        self.fitness_results = list(zip(self.fitness_scores, self.genomes))

    @patch("holland.storage.genomes_and_fitnesses.select_from")
    def test_returns_dictionary_with_generation_specified(self, mock_select):
        """format_genomes_and_fitnesses_for_storage returns a dictionary that includes 'generation': generation_num"""
        generation_num = 5

        output = format_genomes_and_fitnesses_for_storage(generation_num, self.fitness_results)

        self.assertIn("generation", output.keys())
        self.assertEqual(output.get("generation"), generation_num)

    @patch("holland.storage.genomes_and_fitnesses.select_from")
    def test_selects_correct_genomes(self, mock_select):
        """format_genomes_and_fitnesses_for_storage calls select_from with the given top, mid, bottom parameters and random=0"""
        generation_num = 5
        storage_options = {"top": 5, "mid": 1, "bottom": 2, "random": 0, "format": "json"}

        format_genomes_and_fitnesses_for_storage(
            generation_num, self.fitness_results, **storage_options
        )

        self.fitness_results.sort(key=lambda x: x[0])
        mock_select.assert_called_with(
            self.fitness_results,
            top=storage_options["top"],
            mid=storage_options["mid"],
            bottom=storage_options["bottom"],
            random=0,
        )

    @patch("holland.storage.genomes_and_fitnesses.select_from")
    def test_selects_correct_genomes_using_correct_defaults(self, mock_select):
        """format_genomes_and_fitnesses_for_storage calls select_from with the given top, mid, bottom, random parameters, using 0 as a default for each"""
        generation_num = 5
        storage_options = {"format": "json"}

        format_genomes_and_fitnesses_for_storage(
            generation_num, self.fitness_results, **storage_options
        )

        self.fitness_results.sort(key=lambda x: x[0])
        mock_select.assert_called_with(self.fitness_results, top=0, mid=0, bottom=0, random=0)

    @patch(
        "holland.storage.genomes_and_fitnesses.select_from",
        return_value=[(1, {"a": [1]}), (2, {"a": [2]})],
    )
    def test_returns_dictionary_containing_selected_genomes(self, mock_select):
        """format_genomes_and_fitnesses_for_storage palces the output genomes (without scores) of select_from in the returned dictionary as the value of 'genomes'"""
        generation_num = 5
        storage_options = {"top": 5, "mid": 1, "bottom": 2, "format": "json"}
        random.shuffle(
            self.fitness_results
        )  # to make sure format_genomes_and_fitnesses_for_storage sorts

        output = format_genomes_and_fitnesses_for_storage(
            generation_num, self.fitness_results, **storage_options
        )

        self.fitness_results.sort(key=lambda x: x[0])

        actual_results = output.get("results")
        expected_results = mock_select.return_value
        self.assertListEqual(actual_results, expected_results)
