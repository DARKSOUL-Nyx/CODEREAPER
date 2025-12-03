
from typing import Final

DEFAULT_TAX_RATE: Final[float] = 0.15


def calculate_total(price: float, tax_rate: float = DEFAULT_TAX_RATE) -> float:
    """
    Calculates the total price including tax.

    This is a pure function; its output depends only on its inputs,
    making it predictable, testable, and reusable. The tax rate dependency
    is now explicit.

    Args:
        price: The base price of the item.
        tax_rate: The tax rate to apply, as a decimal (e.g., 0.15 for 15%).
                  Defaults to the application's standard rate.

    Returns:
        The total price after applying the tax.
    """
    if price < 0:
        raise ValueError("Price cannot be negative.")
    if not 0 <= tax_rate <= 1:
        # Allowing tax rates outside 0-100% might be a business decision,
        # but validation is good practice.
        raise ValueError("Tax rate must be between 0 and 1.")

    return price * (1 + tax_rate)
