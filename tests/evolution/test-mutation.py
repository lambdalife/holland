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

    @patch.object(Mutator, "mutate_gene")
    def test_calls_mutate_gene_on_each_gene_in_genome(self, mock_mutate_gene):
        """mutate_genome calls mutate_gene on each of the genes in genome"""
        self.mutator.mutate_genome(self.genome)

        expected_calls = [
            call(self.genome[gene_name], self.genome_params[gene_name])
            for gene_name in self.genome.keys()
        ]
        mock_mutate_gene.assert_has_calls(expected_calls)

    @patch.object(Mutator, "mutate_gene")
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

    @patch.object(Mutator, "probabilistically_apply_mutation")
    def test_calls_probabilistically_apply_mutation_on_the_gene_for_numeric_type(
        self, mock_apply_mutation
    ):
        """mutate_gene calls probabilistically_apply_mutation once on the gene, passing the gene value, the mutation function, the mutation_rate, and bounds info"""
        gene = 100.5
        gene_params = {**self.gene_params, "type": "float", "min": 0, "max": 100}
        mutator = Mutator({})

        mutator.mutate_gene(gene, gene_params)

        mock_apply_mutation.assert_called_once_with(gene, gene_params)

    @patch.object(Mutator, "probabilistically_apply_mutation")
    def test_calls_probabilitistically_mutate_value_for_each_element_of_gene_with_correct_args_for_numeric_list_type_with_level_value(
        self, mock_apply_mutation
    ):
        """mutate_gene calls probabilistically_apply_mutation many times, passing each value of the gene, the mutation function, the mutation_rate, and bounds info each time if gene_params["mutation_level"] is "value" """
        gene = [1, 2, 3, 4, 5, 6]
        gene_params = {
            **self.gene_params,
            "type": "[float]",
            "min": 0,
            "max": 100,
            "mutation_level": "value",
        }
        mutator = Mutator({})

        mutator.mutate_gene(gene, gene_params)

        expected_calls = [call(value, gene_params) for value in gene]
        mock_apply_mutation.assert_has_calls(expected_calls)
        self.assertEqual(mock_apply_mutation.call_count, len(expected_calls))

    @patch.object(Mutator, "probabilistically_apply_mutation")
    def test_calls_probabilistically_mutation_value_on_the_gene_for_nonnumeric_type(
        self, mock_apply_mutation
    ):
        """mutate_gene calls probabilistically_apply_mutation once on the gene, passing the gene value, the mutation function, the mutation_rate, and bounds info"""
        gene = True
        gene_params = {**self.gene_params, "type": "bool"}
        mutator = Mutator({})

        mutator.mutate_gene(gene, gene_params)

        mock_apply_mutation.assert_called_once_with(gene, gene_params)

    @patch.object(Mutator, "probabilistically_apply_mutation")
    def test_calls_probabilitistically_mutate_value_for_each_element_of_gene_with_correct_args_for_nonnumeric_list_type_if_level_is_value(
        self, mock_apply_mutation
    ):
        """mutate_gene calls probabilistically_apply_mutation many times, passing each value of the gene, the mutation function, the mutation_rate, and bounds info each time if gene_params["mutation_level"] is "value" """
        gene = [True, True, True, False, True, False]
        gene_params = {**self.gene_params, "type": "[bool]", "mutation_level": "value"}
        mutator = Mutator({})

        mutator.mutate_gene(gene, gene_params)

        expected_calls = [call(value, gene_params) for value in gene]
        mock_apply_mutation.assert_has_calls(expected_calls)
        self.assertEqual(mock_apply_mutation.call_count, len(expected_calls))

    @patch.object(Mutator, "probabilistically_apply_mutation")
    def test_defaults_to_using_value_for_mutation_level_if_not_specified_or_invalid(
        self, mock_apply_mutation
    ):
        """mutate_gene defaults to using "value" for the mutation_level if mutation_level is not specified or given mutation_level is invalid"""
        gene = [True, True, True, False, True, False]
        mutator = Mutator({})

        gene_params_options = [
            {**self.gene_params, "type": "[bool]", "mutation_level": "something else"},
            {**self.gene_params, "type": "[bool]"},
        ]

        for gene_params in gene_params_options:
            mock_apply_mutation.reset_mock()

            mutator.mutate_gene(gene, gene_params)

            expected_calls = [call(value, gene_params) for value in gene]
            mock_apply_mutation.assert_has_calls(expected_calls)
            self.assertEqual(mock_apply_mutation.call_count, len(expected_calls))

    @patch.object(Mutator, "probabilistically_apply_mutation")
    def test_calls_probabilitistically_mutate_value_on_whole_gene_if_mutation_level_is_gene(
        self, mock_apply_mutation
    ):
        """mutate_gene calls probabilistically_apply_mutation once on the whole gene if gene_params["mutation_level"] is "gene" """
        gene = [True, True, True, False, False, True]
        gene_params = {**self.gene_params, "type": "[bool]", "mutation_level": "gene"}
        mutator = Mutator({})

        mutator.mutate_gene(gene, gene_params)

        mock_apply_mutation.assert_called_once_with(gene, gene_params)

    @patch.object(Mutator, "probabilistically_apply_mutation")
    def test_returns_mutated_gene(self, mock_apply_mutation):
        """mutate_gene returns a new gene composed of the outputs of calling probabilistically_apply_mutation on each value of the given gene"""
        gene = [1, 2, 3, 4, 5, 6]
        mutated_targets = [2, 2, 5, 4, 9, 6]
        mock_apply_mutation.side_effect = mutated_targets
        gene_params = {**self.gene_params, "type": "[float]"}
        mutator = Mutator({})

        mutated_gene = mutator.mutate_gene(gene, gene_params)

        expected_mutated_gene = mutated_targets
        self.assertListEqual(mutated_gene, expected_mutated_gene)


class MutatorProbabilisticallyMutateValueTest(unittest.TestCase):
    def test_calls_mutation_function_according_to_mutation_rate(self):
        """probabilistically_apply_mutation calls the mutation_function according to the given mutation_rate"""
        value = 1
        gene_params = {
            "mutation_function": Mock(),
            "mutation_rate": 0.1,
            "type": "bool",
        }
        mutator = Mutator({})

        with patch("random.random", return_value=0.001):
            mutator.probabilistically_apply_mutation(value, gene_params)
            self.assertTrue(gene_params["mutation_function"].called)

        gene_params["mutation_function"].reset_mock()

        with patch("random.random", return_value=0.9):
            mutator.probabilistically_apply_mutation(value, gene_params)
            self.assertFalse(gene_params["mutation_function"].called)

    @patch("random.random", return_value=0.001)
    @patch("holland.evolution.mutation.bound_value")
    def test_bounds_each_element_of_target_if_should_bound_and_target_is_int_list(
        self, mock_bound_value, mock_random
    ):
        """probabilistically_apply_mutation calls bound_value on each element of the mutated target with the correct max, min, and to_int if should_bound is True and target is a list of ints"""
        value = [1, 2, 3, 4, 5]
        gene_params = {
            "mutation_function": Mock(return_value=[100, 200, 300, 400, 500]),
            "mutation_rate": 0.1,
            "type": "[int]",
            "min": 0,
            "max": 10,
        }
        mutator = Mutator({})

        mutator.probabilistically_apply_mutation(value, gene_params)

        expected_calls = [
            call(
                mv, minimum=gene_params["min"], maximum=gene_params["max"], to_int=True
            )
            for mv in gene_params["mutation_function"].return_value
        ]
        mock_bound_value.assert_has_calls(expected_calls)
        self.assertEqual(mock_bound_value.call_count, len(expected_calls))

    @patch("random.random", return_value=0.001)
    @patch("holland.evolution.mutation.bound_value")
    def test_bounds_each_element_of_target_if_should_bound_and_target_is_float_list(
        self, mock_bound_value, mock_random
    ):
        """probabilistically_apply_mutation calls bound_value on each element of the mutated target with the correct max, min, and to_int if should_bound is True and target is a list of floats"""
        value = [1.0, 2.0, 3.0, 4.0, 5.0]
        gene_params = {
            "mutation_function": Mock(return_value=[100.0, 200.0, 300.0, 400.0, 500.0]),
            "mutation_rate": 0.1,
            "type": "[float]",
            "min": 0,
            "max": 10,
        }
        mutator = Mutator({})

        mutator.probabilistically_apply_mutation(value, gene_params)

        expected_calls = [
            call(
                mv, minimum=gene_params["min"], maximum=gene_params["max"], to_int=False
            )
            for mv in gene_params["mutation_function"].return_value
        ]
        mock_bound_value.assert_has_calls(expected_calls)
        self.assertEqual(mock_bound_value.call_count, len(expected_calls))

    @patch("random.random", return_value=0.001)
    @patch("holland.evolution.mutation.bound_value")
    def test_bounds_mutated_target_if_should_bound_on_type_int(
        self, mock_bound_value, mock_random
    ):
        """probabilistically_apply_mutation calls bound_value on the mutated target with the correct max, min, and to_int if should_bound is True and target is an int"""
        value = 1
        gene_params = {
            "mutation_function": Mock(return_value=100),
            "mutation_rate": 0.1,
            "type": "int",
            "min": 0,
            "max": 10,
        }
        mutator = Mutator({})

        mutator.probabilistically_apply_mutation(value, gene_params)

        mock_bound_value.assert_called_with(
            gene_params["mutation_function"].return_value,
            minimum=gene_params["min"],
            maximum=gene_params["max"],
            to_int=True,
        )

    @patch("random.random", return_value=0.001)
    @patch("holland.evolution.mutation.bound_value")
    def test_bounds_mutated_target_if_should_bound_on_type_float(
        self, mock_bound_value, mock_random
    ):
        """probabilistically_apply_mutation calls bound_value on the mutated target with the correct max, min, and to_int if should_bound is True and target is a float"""
        value = 1.0
        gene_params = {
            "mutation_function": Mock(return_value=100.0),
            "mutation_rate": 0.1,
            "type": "float",
            "min": 0,
            "max": 10,
        }
        mutator = Mutator({})

        mutator.probabilistically_apply_mutation(value, gene_params)

        mock_bound_value.assert_called_with(
            gene_params["mutation_function"].return_value,
            minimum=gene_params["min"],
            maximum=gene_params["max"],
            to_int=False,
        )

    @patch("random.random", return_value=0.001)
    @patch("holland.evolution.mutation.bound_value")
    def test_does_not_bound_mutated_target_if_not_should_bound(
        self, mock_bound_value, mock_random
    ):
        """probabilistically_apply_mutation does not call bound_value on the mutated value if should_bound is False"""
        value = 1
        gene_params = {
            "mutation_function": Mock(return_value=100),
            "mutation_rate": 0.1,
            "type": "bool",
            "min": 0,
            "max": 10,
        }
        mutator = Mutator({})

        mutator.probabilistically_apply_mutation(value, gene_params)

        mock_bound_value.assert_not_called()

    @patch("random.random", return_value=0.001)
    @patch("holland.evolution.mutation.bound_value", return_value=10)
    def test_returns_result_of_bound_value_if_mutation_function_called_and_should_bound(
        self, mock_bound_value, mock_random
    ):
        """probabilistically_apply_mutation returns the output of bound_value called on the output of the mutation function if the mutation function was used"""
        value = 1
        gene_params = {
            "mutation_function": Mock(return_value=mock_bound_value.return_value + 90),
            "mutation_rate": 0.1,
            "type": "float",
            "min": 0,
            "max": 10,
        }
        mutator = Mutator({})

        output = mutator.probabilistically_apply_mutation(value, gene_params)

        expected_output = mock_bound_value.return_value
        self.assertEqual(output, expected_output)

    @patch("random.random", return_value=0.001)
    @patch("holland.evolution.mutation.bound_value", return_value=10)
    def test_returns_result_of_mutation_function_if_mutation_function_called_and_not_should_bound(
        self, mock_bound_value, mock_random
    ):
        """probabilistically_apply_mutation returns the output of the mutation function if the mutation function was used"""
        value = 1
        gene_params = {
            "mutation_function": Mock(return_value=mock_bound_value.return_value + 90),
            "mutation_rate": 0.1,
            "type": "bool",
            "min": 0,
            "max": 10,
        }
        mutator = Mutator({})

        output = mutator.probabilistically_apply_mutation(value, gene_params)

        expected_output = gene_params["mutation_function"].return_value
        self.assertEqual(output, expected_output)

    @patch("random.random", return_value=0.9)
    def test_returns_original_value_if_mutation_function_not_called(self, mock_random):
        """probabilistically_apply_mutation returns the original value if the mutation function was not called"""
        value = 1
        gene_params = {
            "mutation_function": Mock(return_value=2),
            "mutation_rate": 0.1,
            "type": "str",
        }
        mutator = Mutator({})

        output = mutator.probabilistically_apply_mutation(value, gene_params)

        expected_output = value
        self.assertEqual(output, expected_output)

    @patch("random.random", return_value=0.01)
    def test_returns_an_int_if_type_is_int_and_mutation_called(self, mock_random):
        """probabilistically_apply_mutation returns an int if the gene type is int or [int]"""
        for gene_type in ["int", "[int]"]:
            value = 1
            gene_params = {
                "mutation_function": Mock(return_value=2.3),
                "mutation_rate": 0.1,
                "type": gene_type,
            }
            mutator = Mutator({})

            output = mutator.probabilistically_apply_mutation(value, gene_params)

            self.assertTrue(isinstance(output, int))
