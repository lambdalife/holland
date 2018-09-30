import unittest
from unittest.mock import patch, Mock, call

from holland.evolution.mutation import (
    mutate_genome,
    mutate_gene,
    probabilistically_mutate_value,
)


class MutateGenomeTest(unittest.TestCase):
    def setUp(self):
        self.genome = {
            "gene1": [1, 2, 3, 4, 5],
            "gene2": [10, 20, 30, 40, 50],
            "gene3": [True, False],
        }
        self.genome_params = {
            "gene1": {"param1": 1, "param2": 2},
            "gene2": {"param1": 1, "param2": 2},
            "gene3": {"param1": 1, "param2": 2},
        }

    @patch("holland.evolution.mutation.mutate_gene")
    def test_calls_mutate_gene_on_each_gene_in_genome(self, mock_mutate_gene):
        """mutate_genome calls mutate_gene on each of the genes in genome"""
        mutate_genome(self.genome, self.genome_params)

        expected_calls = [
            call(self.genome[gene_name], self.genome_params[gene_name])
            for gene_name in self.genome.keys()
        ]
        mock_mutate_gene.assert_has_calls(expected_calls)

    @patch("holland.evolution.mutation.mutate_gene")
    def test_returns_mutated_genome(self, mock_mutate_gene):
        """mutate_genome returns a genome in the same structure as the given genome, but containing the mutated genes"""
        mutated_genes = [
            [11, 22, 33, 44, 55],
            [101, 202, 303, 404, 505],
            [False, False],
        ]
        mock_mutate_gene.side_effect = mutated_genes

        mutated_genome = mutate_genome(self.genome, self.genome_params)

        expected_mutated_genome = {
            "gene1": mutated_genes[0],
            "gene2": mutated_genes[1],
            "gene3": mutated_genes[2],
        }
        self.assertDictEqual(mutated_genome, expected_mutated_genome)


class MutateGeneTest(unittest.TestCase):
    def setUp(self):
        self.gene_params = {"mutation_function": Mock(), "mutation_rate": 0.01}

    @patch("holland.evolution.mutation.probabilistically_mutate_value")
    def test_calls_probabilitistically_mutate_value_for_each_element_of_gene_with_correct_args(
        self, mock_mutate_value
    ):
        """mutate_gene calls probabilistically_mutate_value many times, passing each value of the gene, the mutation function, and the mutation_rate each time"""
        gene = [1, 2, 3, 4, 5, 6]

        mutate_gene(gene, self.gene_params)

        expected_mutation_function = self.gene_params["mutation_function"]
        expected_mutation_rate = self.gene_params["mutation_rate"]
        expected_calls = [
            call(
                value, expected_mutation_function, mutation_rate=expected_mutation_rate
            )
            for value in gene
        ]
        mock_mutate_value.assert_has_calls(expected_calls)

    @patch("holland.evolution.mutation.probabilistically_mutate_value")
    def test_returns_mutated_gene(self, mock_mutate_value):
        """mutate_gene returns a new gene composed of the outputs of calling probabilistically_mutate_value on each value of the given gene"""
        gene = [1, 2, 3, 4, 5, 6]
        mutated_values = [2, 2, 5, 4, 9, 6]
        mock_mutate_value.side_effect = mutated_values

        mutated_gene = mutate_gene(gene, self.gene_params)

        expected_mutated_gene = mutated_values
        self.assertListEqual(mutated_gene, expected_mutated_gene)


class ProbabilisticallyMutateValueTest(unittest.TestCase):
    def test_calls_mutation_function_according_to_mutation_rate(self):
        """probabilistically_mutate_value calls the mutation_function according to the given mutation_rate"""
        value = 1
        mutation_function = Mock()
        mutation_rate = 0.1

        with patch("random.random", return_value=0.001):
            probabilistically_mutate_value(
                value, mutation_function, mutation_rate=mutation_rate
            )
            self.assertTrue(mutation_function.called)

        mutation_function.reset_mock()

        with patch("random.random", return_value=0.9):
            probabilistically_mutate_value(
                value, mutation_function, mutation_rate=mutation_rate
            )
            self.assertFalse(mutation_function.called)

    @patch("random.random", return_value=0.001)
    def test_returns_result_of_mutation_function_if_mutation_function_called(
        self, mock_random
    ):
        """probabilistically_mutate_value returns the output of the mutation function if the mutation function was used"""
        value = 1
        mutation_function = Mock(return_value=2)
        mutation_rate = 0.1

        output = probabilistically_mutate_value(
            value, mutation_function, mutation_rate=mutation_rate
        )

        expected_output = mutation_function.return_value
        self.assertEqual(output, expected_output)

    @patch("random.random", return_value=0.9)
    def test_returns_original_value_if_mutation_function_not_called(self, mock_random):
        """probabilistically_mutate_value returns the original value if the mutation function was not called"""
        value = 1
        mutation_function = Mock(return_value=2)
        mutation_rate = 0.1

        output = probabilistically_mutate_value(
            value, mutation_function, mutation_rate=mutation_rate
        )

        expected_output = value
        self.assertEqual(output, expected_output)
