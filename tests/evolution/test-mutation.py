import unittest
from unittest.mock import patch, Mock, call

from holland.evolution.mutation import *


class MutatorMutateGenomeTest(unittest.TestCase):
    def setUp(self):
        self.genome = {
            "gene1": [1, 2, 3, 4, 5],
            "gene2": [10, 20, 30, 40, 50],
            "gene3": [True, False],
        }
        self.genome_params = {
            "gene1": {"type": "[float]"},
            "gene2": {"type": "[int]"},
            "gene3": {"type": "bool"},
        }
        self.mutator = Mutator(self.genome_params)

    @patch("holland.evolution.mutation.Mutator.mutate_gene")
    def test_calls_mutate_gene_on_each_gene_in_genome(self, mock_mutate_gene):
        """mutate_genome calls mutate_gene on each of the genes in genome"""
        self.mutator.mutate_genome(self.genome)

        expected_calls = [
            call(self.genome[gene_name], self.genome_params[gene_name])
            for gene_name in self.genome.keys()
        ]
        mock_mutate_gene.assert_has_calls(expected_calls)

    @patch("holland.evolution.mutation.Mutator.mutate_gene")
    def test_returns_mutated_genome(self, mock_mutate_gene):
        """mutate_genome returns a genome in the same structure as the given genome, but containing the mutated genes"""
        mutated_genes = [
            [11, 22, 33, 44, 55],
            [101, 202, 303, 404, 505],
            [False, False],
        ]
        mock_mutate_gene.side_effect = mutated_genes

        mutated_genome = self.mutator.mutate_genome(self.genome)

        expected_mutated_genome = {
            "gene1": mutated_genes[0],
            "gene2": mutated_genes[1],
            "gene3": mutated_genes[2],
        }
        self.assertDictEqual(mutated_genome, expected_mutated_genome)


class MutatorMutateGeneTest(unittest.TestCase):
    def setUp(self):
        self.gene_params = {"mutation_function": Mock(), "mutation_rate": 0.01}

    @patch("holland.evolution.mutation.Mutator.probabilistically_mutate_value")
    def test_calls_probabilistically_mutate_value_on_the_gene_for_numeric_type(
        self, mock_mutate_value
    ):
        """mutate_gene calls probabilistically_mutate_value once on the gene, passing the gene value, the mutation function, the mutation_rate, and bounds info"""
        gene = 100.5
        gene_params = {**self.gene_params, "type": "float", "min": 0, "max": 100}
        mutator = Mutator({})

        mutator.mutate_gene(gene, gene_params)

        mock_mutate_value.assert_called_once_with(gene, gene_params)

    @patch("holland.evolution.mutation.Mutator.probabilistically_mutate_value")
    def test_calls_probabilitistically_mutate_value_for_each_element_of_gene_with_correct_args_for_numeric_list_type(
        self, mock_mutate_value
    ):
        """mutate_gene calls probabilistically_mutate_value many times, passing each value of the gene, the mutation function, the mutation_rate, and bounds info each time"""
        gene = [1, 2, 3, 4, 5, 6]
        gene_params = {**self.gene_params, "type": "[float]", "min": 0, "max": 100}
        mutator = Mutator({})

        mutator.mutate_gene(gene, gene_params)

        expected_calls = [call(value, gene_params) for value in gene]
        mock_mutate_value.assert_has_calls(expected_calls)
        self.assertEqual(mock_mutate_value.call_count, len(expected_calls))

    @patch("holland.evolution.mutation.Mutator.probabilistically_mutate_value")
    def test_calls_probabilistically_mutation_value_on_the_gene_for_nonnumeric_type(
        self, mock_mutate_value
    ):
        """mutate_gene calls probabilistically_mutate_value once on the gene, passing the gene value, the mutation function, the mutation_rate, and bounds info"""
        gene = True
        gene_params = {**self.gene_params, "type": "bool"}
        mutator = Mutator({})

        mutator.mutate_gene(gene, gene_params)

        mock_mutate_value.assert_called_once_with(gene, gene_params)

    @patch("holland.evolution.mutation.Mutator.probabilistically_mutate_value")
    def test_calls_probabilitistically_mutate_value_for_each_element_of_gene_with_correct_args_for_nonnumeric_list_type(
        self, mock_mutate_value
    ):
        """mutate_gene calls probabilistically_mutate_value many times, passing each value of the gene, the mutation function, the mutation_rate, and bounds info each time"""
        gene = [True, True, True, False, True, False]
        gene_params = {**self.gene_params, "type": "[bool]"}
        mutator = Mutator({})

        mutator.mutate_gene(gene, gene_params)

        expected_calls = [call(value, gene_params) for value in gene]
        mock_mutate_value.assert_has_calls(expected_calls)
        self.assertEqual(mock_mutate_value.call_count, len(expected_calls))

    @patch("holland.evolution.mutation.Mutator.probabilistically_mutate_value")
    def test_returns_mutated_gene(self, mock_mutate_value):
        """mutate_gene returns a new gene composed of the outputs of calling probabilistically_mutate_value on each value of the given gene"""
        gene = [1, 2, 3, 4, 5, 6]
        mutated_values = [2, 2, 5, 4, 9, 6]
        mock_mutate_value.side_effect = mutated_values
        gene_params = {**self.gene_params, "type": "[float]"}
        mutator = Mutator({})

        mutated_gene = mutator.mutate_gene(gene, gene_params)

        expected_mutated_gene = mutated_values
        self.assertListEqual(mutated_gene, expected_mutated_gene)


class MutatorProbabilisticallyMutateValueTest(unittest.TestCase):
    def test_calls_mutation_function_according_to_mutation_rate(self):
        """probabilistically_mutate_value calls the mutation_function according to the given mutation_rate"""
        value = 1
        gene_params = {
            "mutation_function": Mock(),
            "mutation_rate": 0.1,
            "type": "bool",
        }
        mutator = Mutator({})

        with patch("random.random", return_value=0.001):
            mutator.probabilistically_mutate_value(value, gene_params)
            self.assertTrue(gene_params["mutation_function"].called)

        gene_params["mutation_function"].reset_mock()

        with patch("random.random", return_value=0.9):
            mutator.probabilistically_mutate_value(value, gene_params)
            self.assertFalse(gene_params["mutation_function"].called)

    @patch("random.random", return_value=0.001)
    @patch("holland.evolution.mutation.bound_value")
    def test_bounds_mutated_value_if_should_bound(self, mock_bound_value, mock_random):
        """probabilistically_mutate_value calls bound_value on the mutated value with the correct max and min if should_bound is True"""
        value = 1
        gene_params = {
            "mutation_function": Mock(return_value=100),
            "mutation_rate": 0.1,
            "type": "int",
            "min": 0,
            "max": 10,
        }
        mutator = Mutator({})

        mutator.probabilistically_mutate_value(value, gene_params)

        mock_bound_value.assert_called_with(
            gene_params["mutation_function"].return_value,
            minimum=gene_params["min"],
            maximum=gene_params["max"],
            to_int=True,
        )

    @patch("random.random", return_value=0.001)
    @patch("holland.evolution.mutation.bound_value")
    def test_does_not_bound_mutated_value_if_not_should_bound(
        self, mock_bound_value, mock_random
    ):
        """probabilistically_mutate_value does not call bound_value on the mutated value if should_bound is False"""
        value = 1
        gene_params = {
            "mutation_function": Mock(return_value=100),
            "mutation_rate": 0.1,
            "type": "bool",
            "min": 0,
            "max": 10,
        }
        mutator = Mutator({})

        mutator.probabilistically_mutate_value(value, gene_params)

        mock_bound_value.assert_not_called()

    @patch("random.random", return_value=0.001)
    @patch("holland.evolution.mutation.bound_value", return_value=10)
    def test_returns_result_of_bound_value_if_mutation_function_called_and_should_bound(
        self, mock_bound_value, mock_random
    ):
        """probabilistically_mutate_value returns the output of bound_value called on the output of the mutation function if the mutation function was used"""
        value = 1
        gene_params = {
            "mutation_function": Mock(return_value=mock_bound_value.return_value + 90),
            "mutation_rate": 0.1,
            "type": "float",
            "min": 0,
            "max": 10,
        }
        mutator = Mutator({})

        output = mutator.probabilistically_mutate_value(value, gene_params)

        expected_output = mock_bound_value.return_value
        self.assertEqual(output, expected_output)

    @patch("random.random", return_value=0.001)
    @patch("holland.evolution.mutation.bound_value", return_value=10)
    def test_returns_result_of_mutation_function_if_mutation_function_called_and_not_should_bound(
        self, mock_bound_value, mock_random
    ):
        """probabilistically_mutate_value returns the output of the mutation function if the mutation function was used"""
        value = 1
        gene_params = {
            "mutation_function": Mock(return_value=mock_bound_value.return_value + 90),
            "mutation_rate": 0.1,
            "type": "bool",
            "min": 0,
            "max": 10,
        }
        mutator = Mutator({})

        output = mutator.probabilistically_mutate_value(value, gene_params)

        expected_output = gene_params["mutation_function"].return_value
        self.assertEqual(output, expected_output)

    @patch("random.random", return_value=0.9)
    def test_returns_original_value_if_mutation_function_not_called(self, mock_random):
        """probabilistically_mutate_value returns the original value if the mutation function was not called"""
        value = 1
        gene_params = {
            "mutation_function": Mock(return_value=2),
            "mutation_rate": 0.1,
            "type": "str",
        }
        mutator = Mutator({})

        output = mutator.probabilistically_mutate_value(value, gene_params)

        expected_output = value
        self.assertEqual(output, expected_output)

    @patch("random.random", return_value=0.01)
    def test_returns_an_int_if_type_is_int_and_mutation_called(self, mock_random):
        """probabilistically_mutate_value returns an int if the gene type is int or [int]"""
        for gene_type in ["int", "[int]"]:
            value = 1
            gene_params = {
                "mutation_function": Mock(return_value=2.3),
                "mutation_rate": 0.1,
                "type": gene_type,
            }
            mutator = Mutator({})

            output = mutator.probabilistically_mutate_value(value, gene_params)

            self.assertTrue(isinstance(output, int))
