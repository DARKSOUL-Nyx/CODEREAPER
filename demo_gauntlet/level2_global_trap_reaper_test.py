import sys
import os
import pytest

# This allows the test script to find the module to be tested.
# It adds the parent directory of the current script's directory to the Python path.
# This is useful if you have a project structure like:
# project/
# ├── src/
# │   └── your_code.py
# └── tests/
#     └── test_your_code.py
# You might need to adjust the path depending on your project structure.
# For this example, we assume 'code.py' is in the same directory or accessible.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Assuming the code provided by the user is in a file named 'code.py'
from code import calculate_total, DEFAULT_TAX_RATE


# === Test Suite for calculate_total ===

def test_calculate_total_with_default_tax_rate():
    """
    Tests the function with a standard price, relying on the default tax rate.
    """
    assert calculate_total(price=100.0) == pytest.approx(115.0)
    # Verifying the default rate is what we expect
    assert calculate_total(100.0) == pytest.approx(100.0 * (1 + DEFAULT_TAX_RATE))


def test_calculate_total_with_custom_tax_rate():
    """
    Tests the function's ability to accept and use a custom tax rate.
    """
    assert calculate_total(price=100.0, tax_rate=0.20) == pytest.approx(120.0)


def test_calculate_total_with_zero_price():
    """
    Edge case: If the price is zero, the total should be zero regardless of tax.
    """
    assert calculate_total(price=0.0, tax_rate=0.25) == pytest.approx(0.0)


def test_calculate_total_with_zero_tax_rate():
    """
    Edge case: If the tax rate is zero, the total should equal the original price.
    """
    assert calculate_total(price=123.45, tax_rate=0.0) == pytest.approx(123.45)


def test_calculate_total_with_float_inputs():
    """
    Tests the function with floating point numbers for both price and tax rate
    to ensure correct handling of floating point arithmetic.
    """
    assert calculate_total(price=99.99, tax_rate=0.075) == pytest.approx(107.48925)


def test_calculate_total_with_100_percent_tax():
    """
    Edge case: A 100% tax rate should exactly double the price.
    """
    assert calculate_total(price=75.0, tax_rate=1.0) == pytest.approx(150.0)


def test_calculate_total_with_negative_tax_rate():
    """
    Edge case: A negative tax rate should function as a discount, reducing the price.
    """
    assert calculate_total(price=100.0, tax_rate=-0.10) == pytest.approx(90.0)


def test_calculate_total_with_large_numbers():
    """
    Tests the function's handling of large numerical inputs.
    """
    large_price = 1_000_000_000.0
    tax_rate = 0.50
    expected_total = 1_500_000_000.0
    assert calculate_total(price=large_price, tax_rate=tax_rate) == pytest.approx(expected_total)


def test_calculate_total_raises_value_error_for_negative_price():
    """
    Ensures that a ValueError is raised for negative price input, as specified.
    The 'match' argument checks the exception's error message.
    """
    with pytest.raises(ValueError, match="Price cannot be negative."):
        calculate_total(price=-100.0)

    with pytest.raises(ValueError, match="Price cannot be negative."):
        calculate_total(price=-0.01, tax_rate=0.20)


# A parametrized test can cover multiple cases concisely
@pytest.mark.parametrize(
    "price, tax_rate, expected",
    [
        # description: standard positive case
        (200.0, 0.10, 220.0),
        # description: integer inputs
        (50, 0.05, 52.5),
        # description: zero price
        (0, 0.15, 0.0),
        # description: zero tax rate
        (88.0, 0, 88.0),
        # description: high tax rate
        (10.0, 2.0, 30.0),  # 200% tax
        # description: negative tax rate (discount)
        (500.0, -0.25, 375.0),
        # description: floating point precision
        (19.99, 0.06, 21.1894),
    ],
    ids=[
        "standard_case",
        "integer_inputs",
        "zero_price",
        "zero_tax",
        "high_tax_rate",
        "negative_tax_rate",
        "float_precision",
    ]
)
def test_calculate_total_parametrized_scenarios(price, tax_rate, expected):
    """
    Parametrized test to cover a variety of valid calculation scenarios.
    """
    assert calculate_total(price, tax_rate) == pytest.approx(expected)