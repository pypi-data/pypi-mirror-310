import unittest
from unittest.mock import patch
from valid_input.tools import (
    input_int, input_float, input_option, input_yes_no, input_date, input_with_length, input_list, input_num_in_range,
    input_with_regex, validated_input
)
from datetime import datetime


class TestInputInt(unittest.TestCase):

    @patch("builtins.input", side_effect=["invalid", "1.34", "25"])
    def test_valid_input(self, mock_input):
        result = input_int("Introduce your age: ")
        self.assertEqual(result, 25)

class TestInputFloat(unittest.TestCase):

    @patch("builtins.input", side_effect=["invalid", "1.75"])
    def test_valid_input(self, mock_input):
        result = input_float("What's your height? (in meters): ")
        self.assertAlmostEqual(result, 1.75)


class TestInputOption(unittest.TestCase):

    @patch("builtins.input", side_effect=["invalid", "male"])
    def test_valid_option(self, mock_input):
        result = input_option("What's your sex? (male/female/other): ", ["male", "female", "other"])
        self.assertEqual(result, "male")

    @patch("builtins.input", side_effect=["invalid", "5"])
    def test_original_option_choosen(self, mock_input):
        result = input_option("Choose a number: ", [1, 2, 3, 4, 5])
        self.assertEqual(result, 5)


class TestInputYesNo(unittest.TestCase):

    @patch("builtins.input", side_effect=["maybe", "y"])
    def test_yes_input(self, mock_input):
        result = input_yes_no("Are you a student? (yes/no): ")
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["maybe", "no"])
    def test_no_input(self, mock_input):
        result = input_yes_no("Are you a student? (yes/no): ")
        self.assertFalse(result)


class TestInputDate(unittest.TestCase):

    @patch("builtins.input", side_effect=["2000-01-01"])
    def test_default_format(self, mock_input):
        result = input_date("Introduce your birthday (YYYY-MM-DD): ")
        self.assertEqual(result, datetime(2000, 1, 1))

    @patch("builtins.input", side_effect=["01/01/2000"])
    def test_custom_format(self, mock_input):
        result = input_date("Introduce your birthday (DD/MM/YYYY): ", date_format="%d/%m/%Y")
        self.assertEqual(result, datetime(2000, 1, 1))


class TestInputWithLength(unittest.TestCase):

    @patch("builtins.input", side_effect=["John"])
    def test_valid_input(self, mock_input):
        result = input_with_length("Introduce your name: ", max_length=50)
        self.assertEqual(result, "John")

    @patch("builtins.input", side_effect=["Al", "Alice"])
    def test_retry_on_too_short(self, mock_input):
        result = input_with_length("Introduce your name: ", min_length=3, max_length=50)
        self.assertEqual(result, "Alice")


class TestInputList(unittest.TestCase):

    @patch("builtins.input", side_effect=["", "1,2,3"])
    def test_valid_input(self, mock_input):
        result = input_list("Introduce a list of numbers separated by commas: ", item_validation_func=int)
        self.assertEqual(result, [1, 2, 3])

    @patch("builtins.input", side_effect=[""])
    def test_allow_empty(self, mock_input):
        result = input_list("Introduce a list of numbers separated by commas: ",
                            item_validation_func=int, allow_empty=True)
        self.assertEqual(result, [])


class TestInputNumInRange(unittest.TestCase):

    @patch("builtins.input", side_effect=["150", "25"])
    def test_valid_input(self, mock_input):
        result = input_num_in_range("Introduce your age: ", 0, 120)
        self.assertEqual(result, 25)

    @patch("builtins.input", side_effect=["5.3"])
    def test_allow_float(self, mock_input):
        result = input_num_in_range("Introduce a number: ", 0, 10)
        self.assertAlmostEqual(result, 5.3)

    @patch("builtins.input", side_effect=["5.3", "6"])
    def test_disallow_float(self, mock_input):
        result = input_num_in_range("Introduce a number: ", 0, 10, allow_float=False)
        self.assertEqual(result, 6)


class TestInputWithRegex(unittest.TestCase):

    @patch("builtins.input", side_effect=["invalid", "123456789X"])
    def test_valid_input(self, mock_input):
        result = input_with_regex("Introduce the ISBN of the book: ", r"\d{9}[\d|X]")
        self.assertEqual(result, "123456789X")


class TestValidatedInput(unittest.TestCase):

    @patch("builtins.input", side_effect=["invalid", "3", "4"])
    def test_valid_even_number(self, mock_input):
        def validation_func(value: str):
            value = int(value)
            if value % 2 != 0:
                raise ValueError("The number must be even")
            return value

        result = validated_input("Introduce an even number: ", validation_func)
        self.assertEqual(result, 4)


if __name__ == "__main__":
    unittest.main()
