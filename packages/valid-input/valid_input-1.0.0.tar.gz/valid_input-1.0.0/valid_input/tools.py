from typing import Callable, Any, Iterable, Optional
import re
from datetime import datetime


def _input_with_validation(input_txt: str, validation_func: Callable[[str], Any], error_msg: Optional[str] = None):
    val = None
    while val is None:
        try:
            val = validation_func(input(input_txt))
            break
        except ValueError:
            val = None
        print(error_msg or "This is not a valid input")
    return val


def input_int(input_text: str, error_msg: Optional[str] = None):
    error_msg = error_msg or "Input must be an integer"

    def validation_func(value: str):
        try:
            int_val = int(value)
            if int_val != float(value):
                raise ValueError("Input must be an integer")
            return int_val
        except ValueError:
            raise ValueError("Input must be an integer")

    return _input_with_validation(input_text, validation_func, error_msg)


def input_float(input_text: str, error_msg: Optional[str] = None):
    error_msg = error_msg or "Input must be a number"
    return _input_with_validation(input_text, float, error_msg)


def input_option(input_text: str, options_list: Iterable[Any], error_msg: Optional[str] = None):
    options_dict = {str(option): option for option in options_list}
    if len(options_dict) != len(options_list):
        raise ValueError("")

    def validation_func(value: str):
        if value not in options_dict:
            raise ValueError("Invalid option")
        return options_dict[value]

    if not error_msg:
        if len(options_list) <= 10:
            error_msg = f"Invalid option, valid options are [{', '.join(options_dict.keys())}]"
        else:
            error_msg = None

    return _input_with_validation(input_text, validation_func, error_msg)


def input_yes_no(input_text: str, error_msg: str = None):
    def validation_func(value: str):
        value = value.lower()
        if value in ['yes', 'y']:
            return True
        elif value in ['no', 'n']:
            return False
        else:
            raise ValueError("Input must be 'yes' or 'no'")

    error_msg = error_msg or "Please enter 'yes/y' or 'no/n'"

    return _input_with_validation(input_text, validation_func, error_msg)


def input_date(input_text: str, date_format: str = "%Y-%m-%d", error_msg: str = None):
    def validation_func(value: str):
        try:
            return datetime.strptime(value, date_format)
        except ValueError:
            raise ValueError(f"Date must be in the format {date_format}")

    error_msg = error_msg or f"Enter a date in the format {date_format}"

    return _input_with_validation(input_text, validation_func, error_msg)


def input_with_length(input_text: str, min_length: int = 0, max_length: int = None, error_msg: Optional[str] = None):
    def validation_func(value: str):
        if len(value) < min_length:
            raise ValueError(f"Input must be at least {min_length} characters long")
        if max_length is not None and len(value) > max_length:
            raise ValueError(f"Input must be at most {max_length} characters long")
        return value

    error_msg = error_msg or f"Enter text between {min_length} and {max_length} characters"

    return _input_with_validation(input_text, validation_func, error_msg)


def input_list(input_text: str, item_validation_func: Callable[[str], Any] = str,
               separator: str = ',', allow_empty: bool = False, error_msg: Optional[str] = None):
    def validation_func(value: str):
        if value.strip() == "":
            if allow_empty:
                return []
            else:
                raise ValueError("Not allowed empty list")
            
        items = value.split(separator)
        if not allow_empty and len(items) == 0:
            raise ValueError("Input must not be empty")
        return [item_validation_func(item.strip()) for item in items]

    if not error_msg:
        error_msg = "At least one item is not valid"

        if not allow_empty:
            error_msg += " or input is empty"

    return _input_with_validation(input_text, validation_func, error_msg)


def input_num_in_range(input_text: str, min_value: Optional[float] = None, max_value: Optional[float] = None,
                       allow_float: bool = True, error_msg: Optional[str] = None):

    if min_value is not None and max_value is not None:
        if min_value >= max_value:
            raise ValueError("min_value must be less than max_value")

    def validation_func(value: str):

        if allow_float:
            num = float(value)
        else:
            if int(value) != float(value):
                raise ValueError("Value must be an integer")

            num = int(value)

        if min_value is not None and max_value is not None:
            if not (min_value <= num <= max_value):
                raise ValueError(f"Value must be between {min_value} and {max_value}")
        elif min_value is not None:
            if num < min_value:
                raise ValueError(f"Value must be at least {min_value}")
        elif max_value is not None:
            if num > max_value:
                raise ValueError(f"Value must be at most {max_value}")
        return num

    if not error_msg:
        if min_value is not None and max_value is not None:
            error_msg = f"Enter a number between {min_value} and {max_value}"
        elif min_value is not None:
            error_msg = f"Enter a number at least {min_value}"
        elif max_value is not None:
            error_msg = f"Enter a number at most {max_value}"

        if not allow_float:
            error_msg += " (integer only)"

    return _input_with_validation(input_text, validation_func, error_msg)


def input_with_regex(input_text: str, pattern: str, error_msg: str = None):
    regex = re.compile(pattern)

    def validation_func(value: str):
        if not regex.fullmatch(value):
            raise ValueError("Input does not match the required pattern")
        return value

    return _input_with_validation(input_text, validation_func, error_msg or f"Input must match the pattern: {pattern}")


def validated_input(input_text: str, validation_func: Callable[[str], Any], error_msg: Optional[str] = None):
    return _input_with_validation(input_text, validation_func, error_msg)
