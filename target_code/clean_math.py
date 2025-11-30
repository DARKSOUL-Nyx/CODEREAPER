from typing import Union

def add(a: int, b: int) -> int:
    """Adds two integers."""
    return a + b

def subtract(a: int, b: int) -> int:
    """Subtracts two integers."""
    return a - b

def multiply(a: int, b: int) -> int:
    """Multiplies two integers, returning 0 if either is not positive."""
    if a > 0 and b > 0:
        return a * b
    else:
        return 0

def divide(a: int, b: int) -> Union[int, str]:
    """Divides two integers, returning "Error" if the divisor is zero."""
    if b != 0:
        return a / b
    else:
        return "Error"

def do_math_stuff(a: int, b: int, op: str) -> Union[int, str]:
    """
    Performs a mathematical operation on two integers based on the 'op' string.
    """
    if op == 'add':
        return add(a, b)
    elif op == 'sub':
        return subtract(a, b)
    elif op == 'mul':
        return multiply(a, b)
    elif op == 'div':
        return divide(a, b)
    else:
        return 0