import unittest
from unittest.mock import Mock, call

from holland.evolution.evaluation import *


class EvaluatorEvaluateFitnessTest(unittest.TestCase):
    def test_calls_evaluate_on_each_element_of_gene_pool(self):
        """evaluate_fitness calls fitness_function on each individual in gene_pool"""
        fitness_function = Mock(return_value=1)
        gene_pool = ["a", "b", "c", "d", "e", "f"]
        evaluator = Evaluator(fitness_function)

        evaluator.evaluate_fitness(gene_pool)

        expected_calls = [call(genome) for genome in gene_pool]
        fitness_function.assert_has_calls(expected_calls)

    def test_appends_returned_genome_to_results_if_fitness_function_returns_a_genome(
        self
    ):
        """evaluate_fitness appends the score and genome returned by fitness_function to results if fitness_function returns a tuple/list"""
        gene_pool = ["a", "b", "c", "d", "e", "f"]
        scores = [10, 20, 30, 40, 50, 60]
        final_genomes = ["u", "v", "w", "x", "y", "z"]
        fitness_function = Mock(side_effect=zip(scores, final_genomes))
        evaluator = Evaluator(fitness_function)

        results = evaluator.evaluate_fitness(gene_pool)

        expected_results = list(zip(scores, final_genomes))
        self.assertListEqual(
            sorted(results, key=lambda x: x[0]),
            sorted(expected_results, key=lambda x: x[0]),
        )

    def test_returns_tuples_of_score_and_genome(self):
        """evaluate_fitness pairs each genome with the score received from calling fitness_function on that genome and returns a list of all tuples"""
        scores = [10, 20, 30, 40, 50, 60]
        fitness_function = Mock(side_effect=scores)
        gene_pool = ["a", "b", "c", "d", "e", "f"]
        evaluator = Evaluator(fitness_function)

        results = evaluator.evaluate_fitness(gene_pool)

        expected_results = list(zip(scores, gene_pool))
        self.assertListEqual(
            sorted(results, key=lambda x: x[0]),
            sorted(expected_results, key=lambda x: x[0]),
        )

    def test_returns_results_sorted_by_fitness_score_asc(self):
        """evaluate_fitness returns fitness results in ascending order of fitness if ascending is True"""
        scores = [500, 10, 90, -5, 100, 1]
        fitness_function = Mock(side_effect=scores)
        gene_pool = ["a", "b", "c", "d", "e", "f"]
        evaluator = Evaluator(fitness_function, ascending=True)

        results = evaluator.evaluate_fitness(gene_pool)

        expected_results = sorted(list(zip(scores, gene_pool)), key=lambda x: x[0])
        self.assertListEqual(results, expected_results)

    def test_returns_results_sorted_by_fitness_score_asc_default(self):
        """evaluate_fitness returns fitness results in ascending order of fitness if ascending is not specified"""
        scores = [500, 10, 90, -5, 100, 1]
        fitness_function = Mock(side_effect=scores)
        gene_pool = ["a", "b", "c", "d", "e", "f"]
        evaluator = Evaluator(fitness_function)

        results = evaluator.evaluate_fitness(gene_pool)

        expected_results = sorted(list(zip(scores, gene_pool)), key=lambda x: x[0])
        self.assertListEqual(results, expected_results)

    def test_returns_results_sorted_by_fitness_score_desc(self):
        """evaluate_fitness returns fitness results in descending order of fitness if ascending is False"""
        scores = [500, 10, 90, -5, 100, 1]
        fitness_function = Mock(side_effect=scores)
        gene_pool = ["a", "b", "c", "d", "e", "f"]
        evaluator = Evaluator(fitness_function, ascending=False)

        results = evaluator.evaluate_fitness(gene_pool)

        expected_results = sorted(
            list(zip(scores, gene_pool)), key=lambda x: x[0], reverse=True
        )
        self.assertListEqual(results, expected_results)
