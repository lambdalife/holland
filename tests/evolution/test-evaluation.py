import unittest
from unittest.mock import Mock, call

from holland.evolution.evaluation import evaluate_fitness


class EvaluateFitnessTest(unittest.TestCase):
    def test_calls_evaluate_on_each_element_of_gene_pool(self):
        """evaluate_fitness calls fitness_function on each individual in gene_pool"""
        fitness_function = Mock()
        gene_pool = [1, 2, 3, 4, 5, 6]

        evaluate_fitness(gene_pool, fitness_function)

        expected_calls = [call(genome) for genome in gene_pool]
        fitness_function.assert_has_calls(expected_calls)

    def test_returns_tuples_of_score_and_genome(self):
        """evaluate_fitness pairs each genome with the score received from calling fitness_function on that genome and returns a list of all tuples"""
        scores = [10, 20, 30, 40, 50, 60]
        fitness_function = Mock(side_effect=scores)
        gene_pool = [1, 2, 3, 4, 5, 6]

        results = evaluate_fitness(gene_pool, fitness_function)

        expected_results = list(zip(scores, gene_pool))
        self.assertListEqual(results, expected_results)
