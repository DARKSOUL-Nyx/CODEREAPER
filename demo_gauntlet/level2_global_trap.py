
TAX_RATE = 0.15

def calculate_total(price):
    # Implicitly uses global TAX_RATE
    # If refactored to a pure function without passing TAX_RATE, this breaks.
    return price + (price * TAX_RATE)
