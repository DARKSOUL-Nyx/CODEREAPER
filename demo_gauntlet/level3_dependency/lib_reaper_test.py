import sys
import os
import pytest

# This is a common pattern to make the tested code importable.
# It adds the directory of this test file to the system path.
# It assumes the code to test is in a file (e.g., 'main.py') in the same directory.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Assuming the user's code is in a file named `main.py`
from main import process_data


def test_standard_case_with_mixed_integers():
    """Tests basic filtering and doubling with a list of positive and negative integers."""
    input_data = [1, 6, 4, 8, 5, 10, -2]
    expected = [12, 16, 20]
    assert process_data(input_data) == expected


def test_edge_case_empty_iterable():
    """Tests that an empty iterable correctly returns an empty list."""
    assert process_data([]) == []


def test_edge_case_no_numbers_greater_than_five():
    """Tests an iterable where no numbers meet the filter condition."""
    input_data = [5, 4, 3, 0, -10]
    expected = []
    assert process_data(input_data) == expected


def test_edge_case_all_numbers_greater_than_five():
    """Tests an iterable where all numbers meet the filter condition."""
    input_data = [6, 7, 8, 100]
    expected = [12, 14, 16, 200]
    assert process_data(input_data) == expected


def test_boundary_condition_at_five():
    """Tests the boundary condition, ensuring the number 5 itself is excluded."""
    input_data = [4, 5, 6]
    expected = [12]
    assert process_data(input_data) == expected


@pytest.mark.parametrize(
    "iterable_input, expected_output",
    [
        ((6, 1, 8), [12, 16]),  # Tuple
        ({10, 2, 7, 7}, [20, 14]),  # Set (duplicates are inherently handled)
        (range(4, 9), [12, 14, 16]),  # Range object
        ((x for x in [3, 9, 5, 11]), [18, 22]),  # Generator
    ],
)
def test_with_different_iterable_types(iterable_input, expected_output):
    """Tests that the function works correctly with various iterable types."""
    # For sets, the processing order isn't guaranteed. Sort for a stable test.
    if isinstance(iterable_input, set):
        assert sorted(process_data(iterable_input)) == sorted(expected_output)
    else:
        assert process_data(iterable_input) == expected_output


def test_with_floating_point_numbers():
    """Tests that the function handles floating-point numbers correctly."""
    input_data = [5.1, 10.5, 4.9, 5.0, 6.0]
    expected = [10.2, 21.0, 12.0]
    assert process_data(input_data) == expected


def test_with_large_numbers():
    """Tests with large numbers to ensure no overflow issues (handled by Python)."""
    large_num = 10**20
    input_data = [1, 2, large_num, large_num + 1]
    expected = [large_num * 2, (large_num + 1) * 2]
    assert process_data(input_data) == expected


def test_error_on_incompatible_type_in_iterable():
    """
    Tests that a TypeError is raised for non-numeric data that cannot be compared.
    """
    with pytest.raises(TypeError):
        # The comparison 'number > 5' will fail for the string 'seven'
        process_data([1, 8, "seven", 9])


def test_input_iterable_is_not_mutated():
    """Ensures the original input data structure is not modified (mutated)."""
    original_list = [1, 2, 6, 7]
    list_copy = original_list.copy()

    process_data(original_list)
    assert original_list == list_copy, "The input list should not be mutated."