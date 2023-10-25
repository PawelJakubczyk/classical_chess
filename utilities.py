from typing import Any, Type


def type_validator(arg: Any, expected_type: Type, unique_key: str) -> None:
    if not isinstance(arg, expected_type):
        raise TypeError(f'{unique_key} - {arg} must be of type {expected_type.__name__}')


def range_validator(value: int, value_range: range, unique_key: str) -> None:
    if value not in value_range:
        raise ValueError(f'{unique_key} - {value} must be in the range [{lower_limit}, {upper_limit}]')


def value_options_validator(value: Any, value_list: list, unique_key: str) -> None:
    if value not in value_list:
        raise ValueError(f'{unique_key} - {value} must be one of the following values: {value_list}')
