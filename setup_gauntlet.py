import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"Created: {path}")

# LEVEL 1: Basic Spaghetti Code (Tests the Surgeon)
# Challenge: High Complexity, nested ifs, bad naming.
level_1 = """
def calc(x, y, op):
    if op == 'add':
        return x + y
    elif op == 'sub':
        return x - y
    elif op == 'mul':
        if x > 0:
            if y > 0:
                return x * y
        return 0
    else:
        return None
"""

# LEVEL 2: The Shadowing Trap (Tests the Scope Guardian)
# Challenge: Uses a global variable 'TAX_RATE'. Agent usually forgets to pass it.
level_2 = """
TAX_RATE = 0.15

def calculate_total(price):
    # Implicitly uses global TAX_RATE
    # If refactored to a pure function without passing TAX_RATE, this breaks.
    return price + (price * TAX_RATE)
"""

# LEVEL 3: The Dependency Trap (Tests the Graph Shield)
# Challenge: 'process_data' is imported by 'main.py', so signature cannot change.
level_3_lib = """
def process_data(data):
    # This function is spaghetti, BUT its signature (data) is locked by dependency.
    res = []
    for i in data:
        if i > 5:
            res.append(i * 2)
    return res
"""

level_3_main = """
from lib import process_data

data = [1, 6, 3, 8]
# If the Agent changes process_data to take 2 arguments, this line CRASHES.
result = process_data(data) 
print(result)
"""

# Create the Gauntlet
create_file("demo_gauntlet/level1_spaghetti.py", level_1)
create_file("demo_gauntlet/level2_global_trap.py", level_2)
create_file("demo_gauntlet/level3_dependency/lib.py", level_3_lib)
create_file("demo_gauntlet/level3_dependency/main.py", level_3_main)

print("✅ Gauntlet Created. Ready for Streamlit Demo.")