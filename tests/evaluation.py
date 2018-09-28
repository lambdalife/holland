import unittest
from unittest.mock import Mock, call

from holland.evolve.evaluation import run_evaluation


class RunEvaluationTest(unittest.TestCase):
    def test_calls_evaluate_on_each_element_of_gene_pool(self):
        """run_evaluation calls evaluate on each individual in gene_pool"""
        evaluate = Mock()
        gene_pool = [1, 2, 3, 4, 5, 6]

        run_evaluation(evaluate, gene_pool)

        expected_calls = [call(genome) for genome in gene_pool]
        evaluate.assert_has_calls(expected_calls)

    def test_returns_tuples_of_score_and_genome(self):
        """run_evaluation pairs each genome with the score received from calling evaluate on that genome and returns a list of all tuples"""
        scores = [10, 20, 30, 40, 50, 60]
        evaluate = Mock(side_effect=scores)
        gene_pool = [1, 2, 3, 4, 5, 6]

        results = run_evaluation(evaluate, gene_pool)

        expected_results = list(zip(scores, gene_pool))
        self.assertListEqual(results, expected_results)
