
from typing import Callable, Optional, Dict

# --- Core Operation Functions ---

def _add(x: float, y: float) -> float:
    """Adds two numbers."""
    return x + y

def _subtract(x: float, y: float) -> float:
    """Subtracts the second number from the first."""
    return x - y

def _multiply(x: float, y: float) -> float:
    """
    Multiplies two numbers only if both are positive.

    If either number is zero or negative, the result is 0.
    """
    return x * y if x > 0 and y > 0 else 0.0

# --- Dispatch Table ---

OPERATIONS: Dict[str, Callable[[float, float], float]] = {
    "add": _add,
    "sub": _subtract,
    "mul": _multiply,
}

# --- Main Public Function ---

def calculate(x: float, y: float, operation: str) -> Optional[float]:
    """
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
    """
    operation_func = OPERATIONS.get(operation)

    if operation_func:
        return operation_func(x, y)

    return None
