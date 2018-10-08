import unittest
from unittest.mock import Mock, call

from holland.evolution.evaluation import evaluate_fitness


class EvaluateFitnessTest(unittest.TestCase):
    def test_calls_evaluate_on_each_element_of_gene_pool(self):
        """evaluate_fitness calls fitness_function on each individual in gene_pool"""
        fitness_function = Mock(return_value=1)
        gene_pool = ["a", "b", "c", "d", "e", "f"]

        evaluate_fitness(gene_pool, fitness_function)

        expected_calls = [call(genome) for genome in gene_pool]
        fitness_function.assert_has_calls(expected_calls)

    def test_returns_tuples_of_score_and_genome(self):
        """evaluate_fitness pairs each genome with the score received from calling fitness_function on that genome and returns a list of all tuples"""
        scores = [10, 20, 30, 40, 50, 60]
        fitness_function = Mock(side_effect=scores)
        gene_pool = ["a", "b", "c", "d", "e", "f"]

        results = evaluate_fitness(gene_pool, fitness_function)

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

        results = evaluate_fitness(gene_pool, fitness_function, ascending=True)

        expected_results = sorted(list(zip(scores, gene_pool)), key=lambda x: x[0])
        self.assertListEqual(results, expected_results)

    def test_returns_results_sorted_by_fitness_score_asc_default(self):
        """evaluate_fitness returns fitness results in ascending order of fitness if ascending is not specified"""
        scores = [500, 10, 90, -5, 100, 1]
        fitness_function = Mock(side_effect=scores)
        gene_pool = ["a", "b", "c", "d", "e", "f"]

        results = evaluate_fitness(gene_pool, fitness_function)

        expected_results = sorted(list(zip(scores, gene_pool)), key=lambda x: x[0])
        self.assertListEqual(results, expected_results)

    def test_returns_results_sorted_by_fitness_score_desc(self):
        """evaluate_fitness returns fitness results in descending order of fitness if ascending is False"""
        scores = [500, 10, 90, -5, 100, 1]
        fitness_function = Mock(side_effect=scores)
        gene_pool = ["a", "b", "c", "d", "e", "f"]

        results = evaluate_fitness(gene_pool, fitness_function, ascending=False)

        expected_results = sorted(
            list(zip(scores, gene_pool)), key=lambda x: x[0], reverse=True
        )
        self.assertListEqual(results, expected_results)
