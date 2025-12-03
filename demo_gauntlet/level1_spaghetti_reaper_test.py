import sys
import os
import pytest

# Ensure the source code file can be found by Python's importer
# This is useful if the test script is in a different directory (e.g., a 'tests/' folder)
# We assume the file to be tested is named 'calculator_code.py' and is in the parent directory
# For this example, let's assume it's in the same directory.
# A more robust solution might use relative imports or package structures.
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# To make this script runnable standalone, we'll create the source file it tests.
# In a real scenario, this part would not be in the test file.
source_code = """
from typing import Callable, Optional, Dict

# --- Core Operation Functions ---

def _add(x: float, y: float) -> float:
    \"\"\"Adds two numbers.\"\"\"
    return x + y

def _subtract(x: float, y: float) -> float:
    \"\"\"Subtracts the second number from the first.\"\"\"
    return x - y

def _multiply(x: float, y: float) -> float:
    \"\"\"
    Multiplies two numbers only if both are positive.

    If either number is zero or negative, the result is 0.
    \"\"\"
    return x * y if x > 0 and y > 0 else 0.0

# --- Dispatch Table ---

OPERATIONS: Dict[str, Callable[[float, float], float]] = {
    "add": _add,
    "sub": _subtract,
    "mul": _multiply,
}

# --- Main Public Function ---

def calculate(x: float, y: float, operation: str) -> Optional[float]:
    \"\"\"
    Performs a specified arithmetic operation on two numbers.

    This function acts as a dispatcher, looking up the appropriate
    operation from the OPERATIONS table and executing it.

    Args:
        x: The first operand.
        y: The second operand.
        operation: The string identifier for the operation ('add', 'sub', 'mul').

    Returns:
        The result of the calculation as a float.
        Returns None if the specified operation is not supported.
    \"\"\"
    operation_func = OPERATIONS.get(operation)

    if operation_func:
        return operation_func(x, y)

    return None
"""
with open("calculator_code.py", "w") as f:
    f.write(source_code)

from calculator_code import calculate


# === Test Cases for Standard Valid Operations ===

@pytest.mark.parametrize(
    "x, y, operation, expected",
    [
        # --- Addition Cases ---
        pytest.param(5, 3, "add", 8.0, id="add-positive-integers"),
        pytest.param(-5, -3, "add", -8.0, id="add-negative-integers"),
        pytest.param(5, -3, "add", 2.0, id="add-mixed-sign-integers"),
        pytest.param(10.5, 2.5, "add", 13.0, id="add-positive-floats"),
        pytest.param(-10.5, -2.5, "add", -13.0, id="add-negative-floats"),
        pytest.param(10.5, -2.5, "add", 8.0, id="add-mixed-sign-floats"),
        pytest.param(10, 0, "add", 10.0, id="add-with-zero"),
        pytest.param(0, 10, "add", 10.0, id="add-zero-with-number"),
        pytest.param(0, 0, "add", 0.0, id="add-two-zeros"),
        pytest.param(1e12, 2e12, "add", 3e12, id="add-large-numbers"),


        # --- Subtraction Cases ---
        pytest.param(5, 3, "sub", 2.0, id="sub-positive-integers"),
        pytest.param(3, 5, "sub", -2.0, id="sub-positive-integers-negative-result"),
        pytest.param(-5, -3, "sub", -2.0, id="sub-negative-integers"),
        pytest.param(-3, -5, "sub", 2.0, id="sub-negative-integers-positive-result"),
        pytest.param(5, -3, "sub", 8.0, id="sub-mixed-sign-integers"),
        pytest.param(10.5, 2.5, "sub", 8.0, id="sub-positive-floats"),
        pytest.param(10, 0, "sub", 10.0, id="sub-with-zero"),
        pytest.param(0, 10, "sub", -10.0, id="sub-zero-with-number"),
        pytest.param(0, 0, "sub", 0.0, id="sub-two-zeros"),
        pytest.param(3e12, 1e12, "sub", 2e12, id="sub-large-numbers"),


        # --- Multiplication (Happy Path) ---
        pytest.param(5, 3, "mul", 15.0, id="mul-positive-integers"),
        pytest.param(10.5, 2.0, "mul", 21.0, id="mul-positive-floats"),
        pytest.param(0.5, 0.5, "mul", 0.25, id="mul-positive-fractions"),
        pytest.param(1e12, 2e12, "mul", 2e24, id="mul-large-numbers"),
    ],
)
def test_calculate_valid_operations(x, y, operation, expected):
    """
    Tests the calculate function with a variety of valid inputs and operations.
    Covers addition, subtraction, and the happy path for multiplication.
    """
    result = calculate(x, y, operation)
    assert result == pytest.approx(expected)


# === Test Cases for Multiplication Edge Cases ===

@pytest.mark.parametrize(
    "x, y",
    [
        pytest.param(5, 0, id="mul-second-operand-zero"),
        pytest.param(0, 5, id="mul-first-operand-zero"),
        pytest.param(0, 0, id="mul-both-operands-zero"),
        pytest.param(-5, 3, id="mul-first-operand-negative"),
        pytest.param(5, -3, id="mul-second-operand-negative"),
        pytest.param(-5, -3, id="mul-both-operands-negative"),
        pytest.param(10, -0.0001, id="mul-second-operand-small-negative"),
        pytest.param(-1e12, 1e12, id="mul-large-negative-number"),
    ],
)
def test_calculate_multiply_edge_cases(x, y):
    """
    Tests the special condition of the multiply function where it should return 0
    if any operand is zero or negative.
    """
    assert calculate(x, y, "mul") == 0.0


# === Test Cases for Invalid Operations ===

@pytest.mark.parametrize(
    "operation",
    [
        pytest.param("div", id="unsupported-operation-div"),
        pytest.param("power", id="unsupported-operation-power"),
        pytest.param("ADD", id="case-sensitive-add"),
        pytest.param("Sub", id="case-sensitive-sub"),
        pytest.param(" mul", id="leading-whitespace"),
        pytest.param("add ", id="trailing-whitespace"),
        pytest.param("", id="empty-string-operation"),
        pytest.param("!@#$", id="special-characters-operation"),
    ],
)
def test_calculate_invalid_operation(operation):
    """
    Tests that the calculate function returns None for unsupported,
    malformed, or case-incorrect operation strings.
    """
    assert calculate(10, 5, operation) is None