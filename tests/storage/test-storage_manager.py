import unittest
from unittest.mock import patch

from holland.storage.storage_manager import *


class StorageManagerUpdateStorageTest(unittest.TestCase):
    @patch.object(StorageManager, "update_fitness_storage")
    @patch.object(StorageManager, "update_genome_storage")
    def test_calls_relevant_methods_with_correct_args(
        self, mock_update_genomes, mock_update_fitness
    ):
        """update_storage calls update_fitness_storage and update_genome_storage with the correct arguments"""
        generation_num = 58
        fitness_results = [(100, "a"), (150, "b"), (20, "c")]
        storage_manager = StorageManager()

        storage_manager.update_storage(generation_num, fitness_results)

        mock_update_fitness.assert_called_with(generation_num, fitness_results)
        mock_update_genomes.assert_called_with(generation_num, fitness_results)


class StorageManagerReactToInterruptionTest(unittest.TestCase):
    @patch("holland.storage.storage_manager.record_genomes_and_fitnesses")
    def test_calls_record_genomes_if_should(self, mock_record):
        """react_to_interruption calls record_genomes_and_fitnesses with the generation_num, fitness_results, and genome_storage_options if should_record_on_interrupt is True"""
        generation_num = 58
        fitness_results = [(100, "a"), (150, "b"), (20, "c")]
        genome_storage_options = {
            "file_name": "test.json",
            "path": "test/test",
            "format": "json",
            "should_record_on_interrupt": True,
        }
        storage_manager = StorageManager(genome_storage_options=genome_storage_options)

        storage_manager.react_to_interruption(generation_num, fitness_results)

        mock_record.assert_called_with(
            generation_num, fitness_results, **genome_storage_options
        )

    @patch("holland.storage.storage_manager.record_genomes_and_fitnesses")
    def test_does_not_call_record_genomes_if_should_not(self, mock_record):
        """react_to_interruption does not call record_genomes_and_fitnesses if should not"""
        generation_num = 58
        fitness_results = [(100, "a"), (150, "b"), (20, "c")]
        genome_storage_options = {
            "file_name": "test.json",
            "path": "test/test",
            "format": "json",
            "should_record_on_interrupt": False,
        }
        storage_manager = StorageManager(genome_storage_options=genome_storage_options)

        storage_manager.react_to_interruption(generation_num, fitness_results)

        mock_record.assert_not_called()


class StorageManagerUpdateFitnessStorageTest(unittest.TestCase):
    @patch("holland.storage.storage_manager.record_fitness")
    def test_calls_record_fitness_with_correct_args_if_should(self, mock_record):
        """update_fitness_storage calls record_fitness with the generation_num, fitness_scores (not fitness results), and fitness_storage_options if should_record_fitness is True"""
        generation_num = 58
        fitness_scores = [100, 150, 20]
        genomes = ["a", "b", "c"]
        fitness_results = list(zip(fitness_scores, genomes))
        fitness_storage_options = {
            "file_name": "test.csv",
            "path": "test/test",
            "should_record_fitness": True,
            "format": "csv",
        }
        storage_manager = StorageManager(
            fitness_storage_options=fitness_storage_options
        )

        storage_manager.update_fitness_storage(generation_num, fitness_results)

        mock_record.assert_called_with(
            generation_num, fitness_scores, **fitness_storage_options
        )

    @patch("holland.storage.storage_manager.record_fitness")
    def test_does_not_call_record_fitness_if_should_not(self, mock_record):
        """update_fitness_storage does not call record_fitness if should_record_fitness is False"""
        generation_num = 58
        fitness_scores = (100, 150, 20)
        genomes = ("a", "b", "c")
        fitness_results = list(zip(fitness_scores, genomes))
        fitness_storage_options = {
            "file_name": "test.csv",
            "path": "test/test",
            "should_record_fitness": False,
            "format": "csv",
        }
        storage_manager = StorageManager(
            fitness_storage_options=fitness_storage_options
        )

        storage_manager.update_fitness_storage(generation_num, fitness_results)

        mock_record.assert_not_called()

    @patch("holland.storage.storage_manager.record_fitness", return_value={"stat": 100})
    def test_appends_stats_to_fitness_history_if_memory(self, mock_record):
        """update_fitness_storage appends the returned stats from record_fitness to fitness_history if storage format is memory"""
        generation_num = 58
        fitness_scores = (100, 150, 20)
        genomes = ("a", "b", "c")
        fitness_results = list(zip(fitness_scores, genomes))
        fitness_storage_options = {"should_record_fitness": True, "format": "memory"}
        storage_manager = StorageManager(
            fitness_storage_options=fitness_storage_options
        )

        storage_manager.update_fitness_storage(generation_num, fitness_results)

        self.assertIn(mock_record.return_value, storage_manager.fitness_history)


class StorageManagerUpdateGenomeStorageTest(unittest.TestCase):
    @patch.object(StorageManager, "should_record_genomes_now", return_value=True)
    @patch("holland.storage.storage_manager.record_genomes_and_fitnesses")
    def test_calls_record_genomes_and_fitnesses_with_correct_args_if_should_record_genomes(
        self, mock_record, mock_record_now
    ):
        """update_genome_storage calls record_genomes_and_fitnesses with the generation_num, fitness_scores, and genome_storage_options if should_record_genomes_now return True"""
        generation_num = 58
        fitness_results = [(100, "a"), (150, "b"), (20, "c")]
        genome_storage_options = {
            "file_name": "test.json",
            "path": "test/test",
            "format": "json",
        }
        storage_manager = StorageManager(genome_storage_options=genome_storage_options)

        storage_manager.update_genome_storage(generation_num, fitness_results)

        mock_record.assert_called_with(
            generation_num, fitness_results, **genome_storage_options
        )

    @patch.object(StorageManager, "should_record_genomes_now", return_value=False)
    @patch("holland.storage.storage_manager.record_genomes_and_fitnesses")
    def test_does_not_call_record_genomes_and_fitnesses_if_should_not_record_genomes(
        self, mock_record, mock_record_now
    ):
        """update_genome_storage does not call record_genomes_and_fitnesses if should_record_genomes_now return False"""
        generation_num = 58
        fitness_results = [(100, "a"), (150, "b"), (20, "c")]
        genome_storage_options = {
            "file_name": "test.json",
            "path": "test/test",
            "format": "json",
        }
        storage_manager = StorageManager(genome_storage_options=genome_storage_options)

        storage_manager.update_genome_storage(generation_num, fitness_results)

        mock_record.assert_not_called()


class StorageManagerShouldRecordGenomesNowTest(unittest.TestCase):
    def test_returns_True_if_should_record_now(self):
        """should_record_genomes_now returns True if should record at all and the current generation number is divisible by the recording frequency"""
        storage_manager = StorageManager()
        storage_manager.should_record_genomes = True

        pairs = [(2, 4), (3, 9), (1, 15), (5, 105)]

        for freq, current_gen in pairs:
            storage_manager.genome_recording_frequency = freq
            current_generation_num = current_gen
            self.assertTrue(
                storage_manager.should_record_genomes_now(current_generation_num)
            )

    def test_returns_False_if_should_not_record_now(self):
        """should_record_genomes_now returns False if the current generation number is not divisible by the recording frequency"""
        storage_manager = StorageManager()
        storage_manager.should_record_genomes = True

        pairs = [(2, 5), (3, 11), (7, 15), (5, 13)]

        for freq, current_gen in pairs:
            storage_manager.genome_recording_frequency = freq
            current_generation_num = current_gen
            self.assertFalse(
                storage_manager.should_record_genomes_now(current_generation_num)
            )

    def test_returns_False_if_should_not_record_at_all(self):
        """should_record_genomes_now returns False if should_record_genomes is False"""
        storage_manager = StorageManager()
        storage_manager.should_record_genomes = False

        pairs = [(2, 4), (3, 9), (1, 15), (5, 105), (2, 5), (3, 11), (7, 15), (5, 13)]

        for freq, current_gen in pairs:
            storage_manager.genome_recording_frequency = freq
            current_generation_num = current_gen
            self.assertFalse(
                storage_manager.should_record_genomes_now(current_generation_num)
            )
