import unittest
from unittest.mock import patch, call

from holland.evolution.evolution import evolve


class EvolveTest(unittest.TestCase):
    def setUp(self):
        self.fitness_function = lambda x: 100
        self.genome_params = {
            "gene1": {"type": "bool", "size": 10},
            "gene2": {"type": "float", "size": 100},
        }
        self.selection_strategy = {
            "pool": {"top": 1, "mid": 0, "bottom": 1, "random": 0},
            "parents": {"weighting_function": lambda x: 1, "number": 2},
        }

    def test_asserts_random_per_generation_is_nonnegative(self):
        """evolve raises a ValueError if random_per_generation is negative"""
        with self.assertRaises(ValueError):
            evolve(
                self.fitness_function,
                self.genome_params,
                self.selection_strategy,
                random_per_generation=-1,
            )

    def test_asserts_population_size_and_num_generations_are_at_least_one(self):
        """evolve raises a ValueError if population_size or num_generations is less than 1"""
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
                num_generations=0,
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
        random_per_generation = 1
        num_generations = 10
        initial_population = ["A", "B", "C"]
        generated_populations = [
            [chr(i), chr(i + 1), chr(i + 2)]
            for i in range(66, 66 + num_generations - 1)
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
            num_generations=num_generations,
            population_size=population_size,
            random_per_generation=random_per_generation,
        )

        expected_evaluate_fitness_calls = [
            call(pop, self.fitness_function) for pop in all_populations
        ]
        expected_generate_next_gen_calls = [
            call(
                res,
                self.genome_params,
                self.selection_strategy,
                population_size=population_size,
                random_per_generation=random_per_generation,
            )
            for res in results[
                :-1
            ]  # no population is generated for the last go of evaluating fitness
        ]

        mock_evaluate_fitness.assert_has_calls(expected_evaluate_fitness_calls)
        self.assertEqual(mock_evaluate_fitness.call_count, num_generations)
        mock_generate_next_gen.assert_has_calls(expected_generate_next_gen_calls)
        self.assertEqual(mock_generate_next_gen.call_count, num_generations - 1)

    @patch("holland.evolution.evolution.generate_random_genomes")
    @patch("holland.evolution.evolution.evaluate_fitness")
    @patch("holland.evolution.evolution.generate_next_generation")
    def test_returns_fitness_results_from_last_generation(
        self, mock_generate_next_gen, mock_evaluate_fitness, mock_generate_random
    ):
        """evolve returns the fitness_results from the last generation"""
        num_generations = 10
        initial_population = ["A", "B", "C"]
        generated_populations = [
            [chr(i), chr(i + 1), chr(i + 2)]
            for i in range(66, 66 + num_generations - 1)
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
            num_generations=num_generations,
        )

        expected_final_results = results[-1]
        self.assertListEqual(final_results, expected_final_results)
