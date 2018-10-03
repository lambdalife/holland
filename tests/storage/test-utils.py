import os
import unittest

from holland.storage.utils import record_to_csv


class RecordToCsvTest(unittest.TestCase):
    def setUp(self):
        self.data = {"b": 1, "a": 2, "c": 3}  # weird order on purpose
        self.file_name = "test.csv"
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.full_path = os.path.join(self.path, self.file_name)

    def test_file_name_and_path_are_specified(self):
        """record_to_csv throws an AssertionError if the file_name or path is not specified"""
        with self.assertRaises(AssertionError):
            record_to_csv(self.data, file_name=self.file_name)

        with self.assertRaises(AssertionError):
            record_to_csv(self.data, path=self.path)

        with self.assertRaises(AssertionError):
            record_to_csv(self.data)

    def test_asserts_data_values_are_int_or_float(self):
        """record_to_csv throws a ValueError if the data values are not int or float"""
        with self.assertRaises(ValueError):
            data = {"a": [1, 2, 3]}
            record_to_csv(data, file_name=self.file_name, path=self.path)

        with self.assertRaises(ValueError):
            data = {"a": {"a": 1, "b": 2}}
            record_to_csv(data, file_name=self.file_name, path=self.path)

        with self.assertRaises(ValueError):
            data = {"a": "b"}
            record_to_csv(data, file_name=self.file_name, path=self.path)

    def test_creates_file_with_correct_name_in_correct_path_if_none_exists(self):
        """record_to_csv creates a file with the correct name in the correct path if no file exists yet"""
        record_to_csv(self.data, file_name=self.file_name, path=self.path)

        self.assertTrue(os.path.exists(self.full_path))

    def test_created_file_has_correct_column_names(self):
        """record_to_csv writes the column names and a newline at the top of the file if a file needs to be created"""
        record_to_csv(self.data, file_name=self.file_name, path=self.path)

        with open(self.full_path, "r") as f:
            column_names = f.readlines()[0]

        expected_column_names = ",".join(sorted(self.data.keys())) + "\n"
        self.assertEqual(column_names, expected_column_names)

    def test_writes_values_to_file_in_correct_columns_after_creating_a_file(self):
        """record_to_csv writes the given values and a newline to the specified file after creating that file"""
        record_to_csv(self.data, file_name=self.file_name, path=self.path)

        with open(self.full_path, "r") as f:
            values = f.readlines()[-1]

        expected_values = (
            ",".join(
                [str(v) for k, v in sorted(list(self.data.items()), key=lambda x: x[0])]
            )
            + "\n"
        )
        self.assertEqual(values, expected_values)

    def test_appends_new_values_to_an_existing_file_without_overwriting_anything(self):
        """record_to_csv appends the given values and a newline to the specified file if that file already exists"""
        first_line = "a,b,c\n"
        second_line = "1,1,1\n"
        with open(self.full_path, "w") as f:
            f.write(first_line)
            f.write(second_line)
        data = {"c": 9, "b": 10, "a": 8}

        record_to_csv(data, file_name=self.file_name, path=self.path)

        with open(self.full_path, "r") as f:
            lines = f.readlines()

        expected_num_lines = 3
        self.assertEqual(len(lines), expected_num_lines)
        self.assertEqual(lines[0], first_line)
        self.assertEqual(lines[1], second_line)
        third_line = (
            ",".join(
                [str(v) for k, v in sorted(list(data.items()), key=lambda x: x[0])]
            )
            + "\n"
        )
        self.assertEqual(lines[2], third_line)

    def tearDown(self):
        if os.path.exists(self.full_path):
            os.remove(self.full_path)
