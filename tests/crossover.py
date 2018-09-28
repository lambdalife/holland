import unittest
from unittest.mock import Mock, call

from holland.evolve.crossover import cross


class CrossTest(unittest.TestCase):
    def setUp(self):
        self.genomes = [
            {"gene1": [1, 2, 3, 4], "gene2": [True, False]},
            {"gene1": [5, 6, 7, 8], "gene2": [False, True]},
        ]

    def test_calls_cross_function_on_each_pair_of_matching_genes(self):
        """cross calls the given cross_function on pairs of genes from the two given genomes"""
        cross_function = Mock()

        cross(*self.genomes, cross_function)

        expected_calls = [
            call(self.genomes[0]["gene1"], self.genomes[1]["gene1"]),
            call(self.genomes[0]["gene2"], self.genomes[1]["gene2"]),
        ]
        cross_function.assert_has_calls(expected_calls)

    def test_returns_the_crossed_genome(self):
        """cross returns a new genome composed of genes returned by the cross_function"""
        crossed_genes = [[10, 12, 14, 16], [True, True]]
        cross_function = Mock(side_effect=crossed_genes)

        crossed = cross(*self.genomes, cross_function)

        expected_crossed = {"gene1": crossed_genes[0], "gene2": crossed_genes[1]}
        self.assertDictEqual(crossed, expected_crossed)
