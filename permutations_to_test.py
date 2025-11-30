
from __future__ import annotations

import doctest
from typing import Generator, List, TypeVar

T = TypeVar("T")

def generate_permutations(sequence: List[T]) -> Generator[List[T], None, None]:
    n = len(sequence)
    if n == 0:
        yield []
        return

    used_indices = [False] * n
    current_permutation: List[T] = []

    def _backtrack() -> Generator[List[T], None, None]:
        if len(current_permutation) == n:
            yield list(current_permutation)
            return

        for i in range(n):
            if not used_indices[i]:
                used_indices[i] = True
                current_permutation.append(sequence[i])
                yield from _backtrack()
                current_permutation.pop()
                used_indices[i] = False

    yield from _backtrack()
