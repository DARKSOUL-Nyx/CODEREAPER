import sys
sys.path.append('.')
from clean_math import *
import pytest
from typing import Union

from your_module import add, subtract, multiply, divide, do_math_stuff  # Replace your_module


@pytest.mark.parametrize("a, b, expected", [(2, 3, 5), (-2, -3, -5), (2, -3, -1), (0, 5, 5)])
def test_add(a, b, expected):
    assert add(a, b) == expected


@pytest.mark.parametrize("a, b, expected", [(5, 2, 3), (-5, -2, -3), (5, -2, 7), (0, 5, -5)])
def test_subtract(a, b, expected):
    assert subtract(a, b) == expected


@pytest.mark.parametrize("a, b, expected", [(2, 3, 6), (-2, 3, 0), (2, -3, 0), (0, 5, 0)])
def test_multiply(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.parametrize("a, b, expected", [(6, 2, 3.0), (-6, 2, -3.0), (6, -2, -3.0), (5, 0, "Error"), (0, 5, 0.0)])
def test_divide(a, b, expected):
    assert divide(a, b) == expected


@pytest.mark.parametrize(
    "a, b, op, expected",
    [
        (2, 3, "add", 5),
        (5, 2, "sub", 3),
        (2, 3, "mul", 6),
        (6, 2, "div", 3.0),
        (5, 0, "div", "Error"),
        (2, 3, "invalid", 0),
        (-2, 3, "mul", 0),
        (0, 5, "add", 5),
    ],
)
def test_do_math_stuff(a, b, op, expected):
    assert do_math_stuff(a, b, op) == expected