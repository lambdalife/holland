import unittest
from unittest.mock import Mock, call

from holland.evolution.crossover import *


class CrosserCrossGenomesTest(unittest.TestCase):
    def setUp(self):
        self.genomes = [
            {"gene1": [1, 2, 3, 4], "gene2": [True, False]},
            {"gene1": [5, 6, 7, 8], "gene2": [False, True]},
        ]

    def test_calls_cross_function_on_each_pair_of_matching_genes(self):
        """cross_genomes calls the appropriate crossover_function on pairs of genes from the given genomes"""
        genome_params = {
            "gene1": {"crossover_function": Mock()},
            "gene2": {"crossover_function": Mock()},
        }
        crosser = Crosser(genome_params)

        crosser.cross_genomes(self.genomes)

        genome_params["gene1"]["crossover_function"].assert_called_with(
            [g["gene1"] for g in self.genomes]
        )
        genome_params["gene2"]["crossover_function"].assert_called_with(
            [g["gene2"] for g in self.genomes]
        )

    def test_returns_the_crossed_genome(self):
        """cross_genomes returns a new genome composed of genes returned by the crossover_functions"""
        genome_params = {
            "gene1": {"crossover_function": Mock(return_value=[10, 12, 14, 16])},
            "gene2": {"crossover_function": Mock(return_value=[True, True])},
        }
        crosser = Crosser(genome_params)

        crossed = crosser.cross_genomes(self.genomes)

        expected_crossed = {
            "gene1": genome_params["gene1"]["crossover_function"].return_value,
            "gene2": genome_params["gene2"]["crossover_function"].return_value,
        }
        self.assertDictEqual(crossed, expected_crossed)

    def test_handles_a_single_parent(self):
        """if the given list of parents is a singleton, cross_genomes does not break"""
        genomes = [{"gene1": [1, 2, 3, 4], "gene2": [True, False]}]
        genome_params = {
            "gene1": {"crossover_function": Mock()},
            "gene2": {"crossover_function": Mock()},
        }
        crosser = Crosser(genome_params)

        crosser.cross_genomes(self.genomes)

    def test_handles_more_than_two_parents(self):
        """if the given list of parents contains more than two elements, cross_genomes does not break"""
        genomes = [
            {"gene1": [1, 2, 3, 4], "gene2": [True, False]},
            {"gene1": [3, 2, 3, 4], "gene2": [True, True]},
            {"gene1": [1, 10, 3, 4], "gene2": [False, False]},
        ]
        genome_params = {
            "gene1": {"crossover_function": Mock()},
            "gene2": {"crossover_function": Mock()},
        }
        crosser = Crosser(genome_params)

        crosser.cross_genomes(self.genomes)
