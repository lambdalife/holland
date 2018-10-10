import unittest
from unittest.mock import patch, call

from holland.storage.storage_manager import StorageManager
from holland.evolution.evolution import evolve


class EvolveTest(unittest.TestCase):
    def setUp(self):
        self.fitness_function = lambda x: 100
        self.genome_params = {
            "gene1": {"type": "[bool]", "size": 10},
            "gene2": {"type": "[float]", "size": 100},
        }
        self.selection_strategy = {
            "pool": {"top": 1, "mid": 0, "bottom": 1, "random": 0},
            "parents": {"weighting_function": lambda x: 1, "number": 2},
        }

    def test_asserts_n_random_and_n_elites_per_generation_are_nonnegative(self):
        """evolve raises a ValueError if n_random_per_generation or n_elite_per_generation is negative"""
        with self.assertRaises(ValueError):
            evolve(
                self.fitness_function,
                self.genome_params,
                self.selection_strategy,
                n_random_per_generation=-1,
            )

        with self.assertRaises(ValueError):
            evolve(
                self.fitness_function,
                self.genome_params,
                self.selection_strategy,
                n_elite_per_generation=-1,
            )

    def test_asserts_population_size_and_n_generations_are_at_least_one(self):
        """evolve raises a ValueError if population_size or n_generations is less than 1"""
        with self.assertRaises(ValueError):
            evolve(
                self.fitness_function,
                self.genome_params,
                self.selection_strategy,
                population_size=0,
            )

        with self.assertRaises(ValueError):
            evolve(
                self.fitness_function,
                self.genome_params,
                self.selection_strategy,
                n_generations=0,
            )

    @patch("holland.evolution.evolution.generate_random_genomes")
    @patch("holland.evolution.evolution.evaluate_fitness")
    @patch("holland.evolution.evolution.generate_next_generation")
    def test_generates_random_init_pop_if_not_given_init_pop(
        self, mock_generate_next_gen, mock_evaluate_fitness, mock_generate_random
    ):
        """evolve generates a random initial population if one is not passed as an argument"""
        population_size = 100
        evolve(
            self.fitness_function,
            self.genome_params,
            self.selection_strategy,
            population_size=population_size,
        )

        mock_generate_random.assert_called_with(self.genome_params, population_size)

    @patch("holland.evolution.evolution.generate_random_genomes")
    @patch("holland.evolution.evolution.evaluate_fitness")
    @patch("holland.evolution.evolution.generate_next_generation")
    def test_does_not_generate_random_init_pop_if_given_init_pop(
        self, mock_generate_next_gen, mock_evaluate_fitness, mock_generate_random
    ):
        """evolve does not generate a random initial population if one is passed as an argument"""
        population_size = 100
        initial_population = ["a", "b", "c"]
        evolve(
            self.fitness_function,
            self.genome_params,
            self.selection_strategy,
            population_size=population_size,
            initial_population=initial_population,
        )

        mock_generate_random.assert_not_called()

    @patch("holland.evolution.evolution.generate_random_genomes")
    @patch("holland.evolution.evolution.StorageManager")
    @patch("holland.evolution.evolution.evaluate_fitness")
    @patch("holland.evolution.evolution.generate_next_generation")
    def test_constructs_a_storage_manager_with_the_correct_args(
        self, mock_generate_next_gen, mock_evaluate_fitness, MockStorageManager, mock_generate_random
    ):
        """evolve constructs an instance of StorageManager with the correct arguments"""
        fitness_storage_options = {"file_name": "test.csv"}
        genome_storage_options = {"file_name": "test.json"}

        evolve(
            self.fitness_function,
            self.genome_params,
            self.selection_strategy,
            fitness_storage_options=fitness_storage_options,
            genome_storage_options=genome_storage_options,
        )

        MockStorageManager.assert_called_with(
            fitness_storage_options=fitness_storage_options,
            genome_storage_options=genome_storage_options,
        )

    @patch("holland.evolution.evolution.generate_random_genomes")
    @patch("holland.evolution.evolution.evaluate_fitness")
    @patch("holland.evolution.evolution.generate_next_generation")
    def test_evaluates_fitness_and_generates_new_generation_in_each_generation(
        self, mock_generate_next_gen, mock_evaluate_fitness, mock_generate_random
    ):
        """evolve calls evaluate_fitness on the current population with the given fitness_function in each generation then passes the results to generate_next_generation and so on"""
        population_size = 3
        n_random_per_generation = 1
        n_elite_per_generation = 1
        n_generations = 10
        initial_population = ["A", "B", "C"]
        generated_populations = [
            [chr(i), chr(i + 1), chr(i + 2)] for i in range(66, 66 + n_generations - 1)
        ]
        all_populations = [initial_population] + generated_populations
        results = [list(zip([10, 20, 30], pop)) for pop in all_populations]

        mock_evaluate_fitness.side_effect = results
        mock_generate_next_gen.side_effect = generated_populations

        evolve(
            self.fitness_function,
            self.genome_params,
            self.selection_strategy,
            initial_population=initial_population,
            n_generations=n_generations,
            population_size=population_size,
            n_random_per_generation=n_random_per_generation,
            n_elite_per_generation=n_elite_per_generation,
        )

        expected_evaluate_fitness_calls = [
            call(pop, self.fitness_function, ascending=True) for pop in all_populations
        ]
        expected_generate_next_gen_calls = [
            call(
                res,
                self.genome_params,
                self.selection_strategy,
                population_size=population_size,
                n_random=n_random_per_generation,
                n_elite=n_elite_per_generation,
            )
            for res in results[:-1]
            # no population is generated for the last go of evaluating fitness
        ]

        mock_evaluate_fitness.assert_has_calls(expected_evaluate_fitness_calls)
        self.assertEqual(
            mock_evaluate_fitness.call_count, len(expected_evaluate_fitness_calls)
        )
        mock_generate_next_gen.assert_has_calls(expected_generate_next_gen_calls)
        self.assertEqual(
            mock_generate_next_gen.call_count, len(expected_generate_next_gen_calls)
        )

    @patch("holland.evolution.evolution.generate_random_genomes")
    @patch("holland.evolution.evolution.evaluate_fitness")
    @patch("holland.evolution.evolution.generate_next_generation")
    def test_calls_evaluate_fitness_with_asc_if_maximize(
        self, mock_generate_next_gen, mock_evaluate_fitness, mock_generate_random
    ):
        """evolve calls evalute_fitness with ascending=True if should_maximize_fitness=True"""
        n_generations = 1
        initial_population = ["A", "B", "C"]

        evolve(
            self.fitness_function,
            self.genome_params,
            self.selection_strategy,
            should_maximize_fitness=True,
            initial_population=initial_population,
            n_generations=n_generations,
        )

        mock_evaluate_fitness.assert_called_with(
            initial_population, self.fitness_function, ascending=True
        )

    @patch("holland.evolution.evolution.generate_random_genomes")
    @patch("holland.evolution.evolution.evaluate_fitness")
    @patch("holland.evolution.evolution.generate_next_generation")
    def test_calls_evaluate_fitness_with_asc_False_if_not_maximize(
        self, mock_generate_next_gen, mock_evaluate_fitness, mock_generate_random
    ):
        """evolve calls evalute_fitness with ascending=False if should_maximize_fitness=False"""
        n_generations = 1
        initial_population = ["A", "B", "C"]

        evolve(
            self.fitness_function,
            self.genome_params,
            self.selection_strategy,
            should_maximize_fitness=False,
            initial_population=initial_population,
            n_generations=n_generations,
        )

        mock_evaluate_fitness.assert_called_with(
            initial_population, self.fitness_function, ascending=False
        )

    @patch("holland.evolution.evolution.generate_random_genomes")
    @patch("holland.evolution.evolution.evaluate_fitness")
    @patch.object(StorageManager, "update_storage")
    @patch("holland.evolution.evolution.generate_next_generation")
    def test_calls_storage_manager_update_storage_with_correct_args(
        self,
        mock_generate_next_gen,
        mock_update_storage,
        mock_evaluate_fitness,
        mock_generate_random,
    ):
        """evolve calls StorageManager.update_storage with the generation_num and fitness_results in each generation"""
        n_generations = 10
        fitness_results = [
            [(i + j, chr(65 + i + j)) for j in range(4)] for i in range(n_generations)
        ]
        mock_evaluate_fitness.side_effect = fitness_results

        evolve(
            self.fitness_function,
            self.genome_params,
            self.selection_strategy,
            n_generations=n_generations,
        )

        expected_calls = [call(i, fitness_results[i]) for i in range(n_generations)]
        mock_update_storage.assert_has_calls(expected_calls)
        self.assertEqual(mock_update_storage.call_count, len(expected_calls))

    @patch("holland.evolution.evolution.generate_random_genomes")
    @patch("holland.evolution.evolution.evaluate_fitness", return_value=[1, 2, 3])
    @patch.object(StorageManager, "react_to_interruption")
    @patch("holland.evolution.evolution.generate_next_generation")
    def test_calls_record_genomes_and_fitnesses_on_interrupt_if_should(
        self,
        mock_generate_next_gen,
        mock_react,
        mock_evaluate_fitness,
        mock_generate_random,
    ):
        """evolve calls StorageManager.react_to_interruption if there is an unhandled interruption before re-raising the Exception"""
        n_generations = 10
        interrupt_generation = 4
        mock_evaluate_fitness.side_effect = [
            mock_evaluate_fitness.return_value
        ] * interrupt_generation + [Exception]

        with self.assertRaises(Exception):
            evolve(
                self.fitness_function,
                self.genome_params,
                self.selection_strategy,
                n_generations=n_generations,
            )

        mock_react.assert_called_once_with(
            interrupt_generation, mock_evaluate_fitness.return_value
        )

    @patch("holland.evolution.evolution.generate_random_genomes")
    @patch("holland.evolution.evolution.evaluate_fitness")
    @patch("holland.evolution.evolution.generate_next_generation")
    def test_stores_and_returns_fitness_statistics_if_storage_format_is_memory(
        self, mock_generate_next_gen, mock_evaluate_fitness, mock_generate_random
    ):
        """evolve returns the fitness_history of the StorageManager if should_record_fitness storage format is 'memory'"""
        n_generations = 10
        fitness_storage_options = {"should_record_fitness": True, "format": "memory"}

        with patch("holland.evolution.evolution.StorageManager") as MockStorageManager:
            MockStorageManager.return_value.fitness_history = ["a", "b", "c", "d"]

            _, fitness_history = evolve(
                self.fitness_function,
                self.genome_params,
                self.selection_strategy,
                n_generations=n_generations,
                fitness_storage_options=fitness_storage_options,
            )

            self.assertListEqual(
                fitness_history, MockStorageManager.return_value.fitness_history
            )

    @patch("holland.evolution.evolution.generate_random_genomes")
    @patch("holland.evolution.evolution.evaluate_fitness")
    @patch("holland.evolution.evolution.generate_next_generation")
    def test_returns_fitness_results_from_last_generation(
        self, mock_generate_next_gen, mock_evaluate_fitness, mock_generate_random
    ):
        """evolve returns the fitness_results from the last generation"""
        n_generations = 10
        initial_population = ["A", "B", "C"]
        generated_populations = [
            [chr(i), chr(i + 1), chr(i + 2)] for i in range(66, 66 + n_generations - 1)
        ]
        all_populations = [initial_population] + generated_populations
        results = [list(zip([10, 20, 30], pop)) for pop in all_populations]

        mock_evaluate_fitness.side_effect = results
        mock_generate_next_gen.side_effect = generated_populations

        final_results = evolve(
            self.fitness_function,
            self.genome_params,
            self.selection_strategy,
            initial_population=initial_population,
            n_generations=n_generations,
        )

        expected_final_results = results[-1]
        self.assertListEqual(final_results, expected_final_results)
