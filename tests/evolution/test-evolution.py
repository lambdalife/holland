import logging
import unittest
from unittest.mock import patch, call

from holland.evolution.evolution import *
from holland.evolution.breeding import PopulationGenerator
from holland.storage.storage_manager import StorageManager


class EvolverEvolveTest(unittest.TestCase):
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
        self.generation_params = {"population_size": 100, "n_elite": 5, "n_random": 2}
        self.logging_options = {"level": logging.CRITICAL}

    def test_asserts_n_random_and_n_elites_per_generation_are_nonnegative(self):
        """evolve raises a ValueError if generation_params["n_random"] or generation_params["n_elite"] is negative"""
        evolver = Evolver(
            self.fitness_function, self.genome_params, self.selection_strategy
        )

        with self.assertRaises(ValueError):
            evolver.evolve(generation_params={"n_random": -1})

        with self.assertRaises(ValueError):
            evolver.evolve(generation_params={"n_elite": -1})

    def test_asserts_population_size_and_n_generations_are_at_least_one(self):
        """evolve raises a ValueError if generation_params["population_size"] or stop_conditions["n_generations"] is less than 1"""
        evolver = Evolver(
            self.fitness_function, self.genome_params, self.selection_strategy
        )

        with self.assertRaises(ValueError):
            evolver.evolve(generation_params={"population_size": 0})

        with self.assertRaises(ValueError):
            evolver.evolve(stop_conditions={"n_generations": 0})

    @patch("logging.basicConfig")
    @patch("holland.evolution.evolution.PopulationGenerator")
    @patch("holland.evolution.evolution.Evaluator")
    def test_configures_logging_correctly(
        self, MockEvaluator, MockPopulationGenerator, mock_log_config
    ):
        """evolve passes the logging_options to logging.basicConfig as keyword arguments"""
        logging_options = {"filename": "test.out", "level": logging.CRITICAL}
        evolver = Evolver(
            self.fitness_function, self.genome_params, self.selection_strategy
        )

        evolver.evolve(logging_options=logging_options)

        mock_log_config.assert_called_with(**logging_options)

    @patch("logging.getLogger")
    @patch("holland.evolution.evolution.PopulationGenerator")
    @patch("holland.evolution.evolution.Evaluator")
    def test_creates_Logger_instance_correctly(
        self, MockEvaluator, MockPopulationGenerator, mock_get_logger
    ):
        """evolve gets a logger by calling logging.getLogger with name as filename, e.g. holland.evolution.evolution"""
        evolver = Evolver(
            self.fitness_function, self.genome_params, self.selection_strategy
        )

        evolver.evolve(logging_options=self.logging_options)

        expected_name = "holland.evolution.evolution"
        mock_get_logger.assert_called_with(expected_name)

    @patch("holland.evolution.evolution.PopulationGenerator")
    @patch("holland.evolution.evolution.Evaluator")
    def test_creates_PopulationGenerator_instance_correctly(
        self, MockEvaluator, MockPopulationGenerator
    ):
        """evolve creates an instance of the PopulationGenerator class and passes the genome_params, selection_strategy, and generation_params to the constructor"""
        evolver = Evolver(
            self.fitness_function, self.genome_params, self.selection_strategy
        )

        evolver.evolve(
            generation_params=self.generation_params,
            logging_options=self.logging_options,
        )

        MockPopulationGenerator.assert_called_with(
            self.genome_params,
            self.selection_strategy,
            generation_params=self.generation_params,
        )

    @patch.object(PopulationGenerator, "generate_random_genomes")
    @patch("holland.evolution.evolution.Evaluator")
    @patch.object(PopulationGenerator, "generate_next_generation")
    def test_generates_random_init_pop_if_not_given_init_pop(
        self, mock_generate_next_gen, MockEvaluator, mock_generate_random
    ):
        """evolve generates a random initial population if one is not passed as an argument"""
        evolver = Evolver(
            self.fitness_function, self.genome_params, self.selection_strategy
        )
        population_size = 100

        evolver.evolve(
            generation_params={"population_size": population_size},
            logging_options=self.logging_options,
        )

        mock_generate_random.assert_called_with(population_size)

    @patch.object(PopulationGenerator, "generate_random_genomes")
    @patch("holland.evolution.evolution.Evaluator")
    @patch.object(PopulationGenerator, "generate_next_generation")
    def test_does_not_generate_random_init_pop_if_given_init_pop(
        self, mock_generate_next_gen, MockEvaluator, mock_generate_random
    ):
        """evolve does not generate a random initial population if one is passed as an argument"""
        population_size = 100
        initial_population = ["a", "b", "c"]
        evolver = Evolver(
            self.fitness_function, self.genome_params, self.selection_strategy
        )

        evolver.evolve(
            generation_params={"population_size": population_size},
            initial_population=initial_population,
            logging_options=self.logging_options,
        )

        mock_generate_random.assert_not_called()

    @patch.object(PopulationGenerator, "generate_random_genomes")
    @patch("holland.evolution.evolution.Evaluator")
    @patch.object(PopulationGenerator, "generate_next_generation")
    def test_creates_Evaluator_instance_correctly_if_maximize_fitness(
        self, mock_generate_next_gen, MockEvaluator, mock_generate_random
    ):
        """evolve creates an instance of the Evaluator class and passes the fitness function and asc=True to the constructor if should_maximize_fitness is True"""
        evolver = Evolver(
            self.fitness_function,
            self.genome_params,
            self.selection_strategy,
            should_maximize_fitness=True,
        )

        evolver.evolve(logging_options=self.logging_options)

        MockEvaluator.assert_called_with(self.fitness_function, ascending=True)

    @patch.object(PopulationGenerator, "generate_random_genomes")
    @patch("holland.evolution.evolution.Evaluator")
    @patch.object(PopulationGenerator, "generate_next_generation")
    def test_creates_Evaluator_instance_correctly_if_minimize_fitness(
        self, mock_generate_next_gen, MockEvaluator, mock_generate_random
    ):
        """evolve creates an instance of the Evaluator class and passes the fitness function and asc=False to the constructor if should_maximize_fitness is False"""
        evolver = Evolver(
            self.fitness_function,
            self.genome_params,
            self.selection_strategy,
            should_maximize_fitness=False,
        )

        evolver.evolve(logging_options=self.logging_options)

        MockEvaluator.assert_called_with(self.fitness_function, ascending=False)

    @patch.object(PopulationGenerator, "generate_random_genomes")
    @patch.object(Evaluator, "evaluate_fitness")
    @patch.object(PopulationGenerator, "generate_next_generation")
    def test_evaluates_fitness_and_generates_new_generation_in_each_generation(
        self, mock_generate_next_gen, mock_evaluate_fitness, mock_generate_random
    ):
        """evolve calls evaluate_fitness on the current population with the given fitness_function in each generation then passes the results to generate_next_generation and so on"""
        population_size = 3
        n_random_per_generation = 1
        n_elite_per_generation = 1
        generation_params = {
            "population_size": population_size,
            "n_random": n_random_per_generation,
            "n_elite": n_elite_per_generation,
        }
        n_generations = 10
        initial_population = ["A", "B", "C"]
        generated_populations = [
            [chr(i), chr(i + 1), chr(i + 2)] for i in range(66, 66 + n_generations - 1)
        ]
        all_populations = [initial_population] + generated_populations
        results = [list(zip([10, 20, 30], pop)) for pop in all_populations]

        mock_evaluate_fitness.side_effect = results
        mock_generate_next_gen.side_effect = generated_populations

        evolver = Evolver(
            self.fitness_function, self.genome_params, self.selection_strategy
        )

        evolver.evolve(
            initial_population=initial_population,
            stop_conditions={"n_generations": n_generations},
            generation_params=generation_params,
            logging_options=self.logging_options,
        )

        expected_evaluate_fitness_calls = [call(pop) for pop in all_populations]
        expected_generate_next_gen_calls = [
            call(res)
            for res in results[:-1]
            # execution stops before generating a new population on the last gen
        ]

        mock_evaluate_fitness.assert_has_calls(expected_evaluate_fitness_calls)
        self.assertEqual(
            mock_evaluate_fitness.call_count, len(expected_evaluate_fitness_calls)
        )
        mock_generate_next_gen.assert_has_calls(expected_generate_next_gen_calls)
        self.assertEqual(
            mock_generate_next_gen.call_count, len(expected_generate_next_gen_calls)
        )

    @patch.object(PopulationGenerator, "generate_random_genomes")
    @patch.object(logging.Logger, "info")
    @patch.object(Evaluator, "evaluate_fitness")
    @patch.object(PopulationGenerator, "generate_next_generation")
    def test_logs_generation_num_and_max_fitness_on_each_generation(
        self,
        mock_generate_next_gen,
        mock_evaluate_fitness,
        mock_info_log,
        mock_generate_random,
    ):
        """evolve logs the generation number and best fitness score at info level in each generation"""
        n_generations = 17
        scores = [[(i * 10, "a")] for i in range(n_generations + 10)]
        mock_evaluate_fitness.side_effect = scores
        evolver = Evolver(
            self.fitness_function, self.genome_params, self.selection_strategy
        )

        evolver.evolve(
            stop_conditions={"n_generations": n_generations},
            logging_options=self.logging_options,
        )

        expected_calls = [
            call(f"Generation: {i}; Top Score: {scores[i][-1][0]}")
            for i in range(n_generations)
        ]
        mock_info_log.assert_has_calls(expected_calls)

    @patch.object(PopulationGenerator, "generate_random_genomes")
    @patch.object(Evaluator, "evaluate_fitness")
    @patch.object(PopulationGenerator, "generate_next_generation")
    def test_stops_on_reaching_n_generations(
        self, mock_generate_next_gen, mock_evaluate_fitness, mock_generate_random
    ):
        """evolve stops when hitting the specified generation number from stop_conditions["n_generations"]"""
        n_generations = 15
        evolver = Evolver(
            self.fitness_function, self.genome_params, self.selection_strategy
        )

        evolver.evolve(stop_conditions={"n_generations": n_generations})

        self.assertEqual(mock_evaluate_fitness.call_count, n_generations)

    @patch.object(PopulationGenerator, "generate_random_genomes")
    @patch.object(Evaluator, "evaluate_fitness")
    @patch.object(PopulationGenerator, "generate_next_generation")
    def test_stops_on_reaching_target_fitness(
        self, mock_generate_next_gen, mock_evaluate_fitness, mock_generate_random
    ):
        """evolve stops when the max fitness is equal to the target fitness from stop_conditions["n_generations"]"""
        target_fitness = 15
        target_generations = 20
        mock_evaluate_fitness.side_effect = [
            [(1, "a")] if i < target_generations - 1 else [(target_fitness, "b")]
            for i in range(target_generations)
        ]
        evolver = Evolver(
            self.fitness_function, self.genome_params, self.selection_strategy
        )

        evolver.evolve(
            stop_conditions={"target_fitness": target_fitness},
            logging_options=self.logging_options,
        )

        self.assertEqual(mock_evaluate_fitness.call_count, target_generations)

    @patch.object(PopulationGenerator, "generate_random_genomes")
    @patch("holland.evolution.evolution.StorageManager")
    @patch.object(Evaluator, "evaluate_fitness")
    @patch.object(PopulationGenerator, "generate_next_generation")
    def test_constructs_a_storage_manager_with_the_correct_args(
        self,
        mock_generate_next_gen,
        mock_evaluate_fitness,
        MockStorageManager,
        mock_generate_random,
    ):
        """evolve constructs an instance of StorageManager with the correct arguments"""
        fitness_storage_options = {"file_name": "test.csv"}
        genome_storage_options = {"file_name": "test.json"}
        evolver = Evolver(
            self.fitness_function, self.genome_params, self.selection_strategy
        )

        evolver.evolve(
            storage_options={
                "fitness": fitness_storage_options,
                "genomes": genome_storage_options,
            },
            logging_options=self.logging_options,
        )

        MockStorageManager.assert_called_with(
            fitness_storage_options=fitness_storage_options,
            genome_storage_options=genome_storage_options,
        )

    @patch.object(PopulationGenerator, "generate_random_genomes")
    @patch.object(Evaluator, "evaluate_fitness")
    @patch.object(StorageManager, "update_storage")
    @patch.object(PopulationGenerator, "generate_next_generation")
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
        evolver = Evolver(
            self.fitness_function, self.genome_params, self.selection_strategy
        )

        evolver.evolve(
            stop_conditions={"n_generations": n_generations},
            logging_options=self.logging_options,
        )

        expected_calls = [call(i, fitness_results[i]) for i in range(n_generations)]
        mock_update_storage.assert_has_calls(expected_calls)
        self.assertEqual(mock_update_storage.call_count, len(expected_calls))

    @patch.object(PopulationGenerator, "generate_random_genomes")
    @patch.object(Evaluator, "evaluate_fitness", return_value=[[1], [2], [3]])
    @patch.object(StorageManager, "react_to_interruption")
    @patch.object(PopulationGenerator, "generate_next_generation")
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
        evolver = Evolver(
            self.fitness_function, self.genome_params, self.selection_strategy
        )

        with self.assertRaises(Exception):
            evolver.evolve(
                stop_conditions={"n_generations": n_generations},
                logging_options=self.logging_options,
            )

        mock_react.assert_called_once_with(
            interrupt_generation, mock_evaluate_fitness.return_value
        )

    @patch.object(PopulationGenerator, "generate_random_genomes")
    @patch.object(Evaluator, "evaluate_fitness")
    @patch.object(PopulationGenerator, "generate_next_generation")
    def test_stores_and_returns_fitness_statistics_if_storage_format_is_memory(
        self, mock_generate_next_gen, mock_evaluate_fitness, mock_generate_random
    ):
        """evolve returns the fitness_history of the StorageManager if should_record_fitness storage format is 'memory'"""
        n_generations = 10
        storage_options = {
            "fitness": {"should_record_fitness": True, "format": "memory"}
        }
        evolver = Evolver(
            self.fitness_function, self.genome_params, self.selection_strategy
        )

        with patch("holland.evolution.evolution.StorageManager") as MockStorageManager:
            MockStorageManager.return_value.fitness_history = ["a", "b", "c", "d"]

            _, fitness_history = evolver.evolve(
                stop_conditions={"n_generations": n_generations},
                storage_options=storage_options,
                logging_options=self.logging_options,
            )

            self.assertListEqual(
                fitness_history, MockStorageManager.return_value.fitness_history
            )

    @patch.object(PopulationGenerator, "generate_random_genomes")
    @patch.object(Evaluator, "evaluate_fitness")
    @patch.object(PopulationGenerator, "generate_next_generation")
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

        evolver = Evolver(
            self.fitness_function, self.genome_params, self.selection_strategy
        )

        final_results = evolver.evolve(
            initial_population=initial_population,
            stop_conditions={"n_generations": n_generations},
            logging_options=self.logging_options,
        )

        expected_final_results = results[-1]
        self.assertListEqual(final_results, expected_final_results)
