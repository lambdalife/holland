import unittest
from unittest.mock import patch, call

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
    @patch("holland.evolution.evolution.record_fitness")
    @patch("holland.evolution.evolution.generate_next_generation")
    def test_calls_record_fitness_with_correct_args_should_record_fitness(
        self,
        mock_generate_next_gen,
        mock_record_fitness,
        mock_evaluate_fitness,
        mock_generate_random,
    ):
        """evolve calls record_fitness in each generation with the generation_num, fitness_scores, and fitness_storage_options if fitness_storage_options['should_record_fitness'] is True"""
        n_generations = 10
        fitness_storage_options = {
            "file_name": "test.csv",
            "path": "test/test",
            "should_record_fitness": True,
            "format": "csv",
        }
        fitness_results = [
            [(i + j, chr(65 + i + j)) for j in range(4)] for i in range(n_generations)
        ]
        mock_evaluate_fitness.side_effect = fitness_results

        evolve(
            self.fitness_function,
            self.genome_params,
            self.selection_strategy,
            n_generations=n_generations,
            fitness_storage_options=fitness_storage_options,
        )

        fitness_scores = [
            [s for s, g in fitness_result] for fitness_result in fitness_results
        ]
        expected_calls = [
            call(i, fitness_scores[i], **fitness_storage_options)
            for i in range(n_generations)
        ]
        mock_record_fitness.assert_has_calls(expected_calls)
        self.assertEqual(mock_record_fitness.call_count, len(expected_calls))

    @patch("holland.evolution.evolution.generate_random_genomes")
    @patch("holland.evolution.evolution.evaluate_fitness")
    @patch("holland.evolution.evolution.record_fitness")
    @patch("holland.evolution.evolution.generate_next_generation")
    def test_does_not_call_record_fitness_if_should_not(
        self,
        mock_generate_next_gen,
        mock_record_fitness,
        mock_evaluate_fitness,
        mock_generate_random,
    ):
        """evolve does not call record_fitness if fitness_storage_options['should_record_fitness'] is False or not specified"""
        n_generations = 10
        fitness_storage_options_options = [{"should_record_fitness": False}, {}]

        for fitness_storage_options in fitness_storage_options_options:
            evolve(
                self.fitness_function,
                self.genome_params,
                self.selection_strategy,
                n_generations=n_generations,
                fitness_storage_options=fitness_storage_options,
            )

            mock_record_fitness.assert_not_called()

    @patch("holland.evolution.evolution.generate_random_genomes")
    @patch("holland.evolution.evolution.evaluate_fitness")
    @patch("holland.evolution.evolution.record_genomes_and_fitnesses")
    @patch("holland.evolution.evolution.generate_next_generation")
    def test_calls_record_genomes_and_fitnesses_with_correct_args_should_record_genomes(
        self,
        mock_generate_next_gen,
        mock_record_genomes_and_fitnesses,
        mock_evaluate_fitness,
        mock_generate_random,
    ):
        """evolve calls record_genomes_and_fitnesses in each generation with the generation_num, fitness_scores, and genome_storage_options if genome_storage_options['should_record_genomes'] is True"""
        n_generations = 10
        genome_storage_options = {
            "file_name": "test.json",
            "path": "test/test",
            "should_record_genomes": True,
            "record_every_n_generations": 1,
            "format": "json",
        }
        fitness_results = [
            [(i + j, chr(65 + i + j)) for j in range(4)] for i in range(n_generations)
        ]
        mock_evaluate_fitness.side_effect = fitness_results

        evolve(
            self.fitness_function,
            self.genome_params,
            self.selection_strategy,
            n_generations=n_generations,
            genome_storage_options=genome_storage_options,
        )

        expected_calls = [
            call(i, fitness_results[i], **genome_storage_options)
            for i in range(n_generations)
        ]
        mock_record_genomes_and_fitnesses.assert_has_calls(expected_calls)
        self.assertEqual(
            mock_record_genomes_and_fitnesses.call_count, len(expected_calls)
        )

    @patch("holland.evolution.evolution.generate_random_genomes")
    @patch("holland.evolution.evolution.evaluate_fitness")
    @patch("holland.evolution.evolution.record_genomes_and_fitnesses")
    @patch("holland.evolution.evolution.generate_next_generation")
    def test_does_not_call_record_genomes_and_fitnesses_if_should_not_at_all(
        self,
        mock_generate_next_gen,
        mock_record_genomes_and_fitnesses,
        mock_evaluate_fitness,
        mock_generate_random,
    ):
        """evolve does not call record_genomes_and_fitnesses if genome_storage_options['should_record_genomes'] is False or not specified or generation_num is not right"""
        n_generations = 10
        genome_storage_options_options = [{"should_record_genomes": False}, {}]

        for genome_storage_options in genome_storage_options_options:
            evolve(
                self.fitness_function,
                self.genome_params,
                self.selection_strategy,
                n_generations=n_generations,
                genome_storage_options=genome_storage_options,
            )

            mock_record_genomes_and_fitnesses.assert_not_called()

    @patch("holland.evolution.evolution.generate_random_genomes")
    @patch("holland.evolution.evolution.evaluate_fitness")
    @patch("holland.evolution.evolution.record_genomes_and_fitnesses")
    @patch("holland.evolution.evolution.generate_next_generation")
    def test_does_not_call_record_genomes_if_generation_num_is_not_right(
        self,
        mock_generate_next_gen,
        mock_record_genomes_and_fitnesses,
        mock_evaluate_fitness,
        mock_generate_random,
    ):
        """evolve does not call record_genomes_and_fitnesses if generation_number % genome_storage_options['record_every_n_generations'] != 0"""
        n_generations = 10
        record_every = 2
        genome_storage_options = {
            "should_record_genomes": True,
            "record_every_n_generations": record_every,
        }

        evolve(
            self.fitness_function,
            self.genome_params,
            self.selection_strategy,
            n_generations=n_generations,
            genome_storage_options=genome_storage_options,
        )

        expected_calls = [
            call(i, mock_evaluate_fitness.return_value, **genome_storage_options)
            for i in range(0, n_generations, record_every)
        ]

    @patch("holland.evolution.evolution.generate_random_genomes")
    @patch("holland.evolution.evolution.evaluate_fitness", return_value=[1, 2, 3])
    @patch("holland.evolution.evolution.record_genomes_and_fitnesses")
    @patch("holland.evolution.evolution.generate_next_generation")
    def test_calls_record_genomes_and_fitnesses_on_interrupt_if_should(
        self,
        mock_generate_next_gen,
        mock_record_genomes_and_fitnesses,
        mock_evaluate_fitness,
        mock_generate_random,
    ):
        """evolve calls record_genomes_and_fitnesses if there is an unhandled interruption before re-raising the Exception"""
        n_generations = 10
        genome_storage_options = {
            "should_record_on_interrupt": True,
            "file_name": "test.json",
            "record_every_n_generations": 20,
        }
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
                genome_storage_options=genome_storage_options,
            )

        expected_calls = [
            call(
                interrupt_generation,
                mock_evaluate_fitness.return_value,
                **genome_storage_options
            )
        ]
        mock_record_genomes_and_fitnesses.assert_has_calls(expected_calls)

    @patch("holland.evolution.evolution.generate_random_genomes")
    @patch("holland.evolution.evolution.evaluate_fitness", return_value=[1, 2, 3])
    @patch("holland.evolution.evolution.record_genomes_and_fitnesses")
    @patch("holland.evolution.evolution.generate_next_generation")
    def test_does_not_call_record_genomes_and_fitnesses_on_interrupt_if_should_not(
        self,
        mock_generate_next_gen,
        mock_record_genomes_and_fitnesses,
        mock_evaluate_fitness,
        mock_generate_random,
    ):
        """evolve does not call record_genomes_and_fitnesses if should_record_on_interrupt is False or not specified"""
        n_generations = 10
        genome_storage_options_options = [
            {
                "should_record_on_interrupt": False,
                "file_name": "test.json",
                "record_every_n_generations": 20,
            },
            {"file_name": "test.json", "record_every_n_generations": 20},
        ]

        for genome_storage_options in genome_storage_options_options:
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
                    genome_storage_options=genome_storage_options,
                )

            mock_record_genomes_and_fitnesses.assert_not_called()

    @patch("holland.evolution.evolution.generate_random_genomes")
    @patch("holland.evolution.evolution.evaluate_fitness")
    @patch("holland.evolution.evolution.record_fitness")
    @patch("holland.evolution.evolution.generate_next_generation")
    def test_stores_and_returns_fitness_statistics_if_storage_format_is_memory(
        self,
        mock_generate_next_gen,
        mock_record_fitness,
        mock_evaluate_fitness,
        mock_generate_random,
    ):
        """evolve appends the returned fitness_statistics from record_fitness to fitness_history and returns fitness_history if storage format is 'memory'"""
        n_generations = 10
        fitness_storage_options = {"should_record_fitness": True, "format": "memory"}
        fitness_results = [
            [(i + j, chr(65 + i + j)) for j in range(4)] for i in range(n_generations)
        ]
        mock_evaluate_fitness.side_effect = fitness_results

        all_fitness_stats = [{"gen": i, "max": i} for i in range(n_generations)]
        mock_record_fitness.side_effect = all_fitness_stats

        _, fitness_history = evolve(
            self.fitness_function,
            self.genome_params,
            self.selection_strategy,
            n_generations=n_generations,
            fitness_storage_options=fitness_storage_options,
        )

        self.assertListEqual(fitness_history, all_fitness_stats)

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
