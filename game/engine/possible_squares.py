from typing import Tuple


class PossibleSquares:

    def __init__(self, possible: set | None = None, n: int = 15, diff: int = 2):
        self.possible_squares: set = possible if possible else set()
        self.n = n
        self.diff = diff

    def update(self, coords: Tuple[int, int]):
        new = set([(i, j) for i in range(coords[0] - self.diff, coords[0] + self.diff + 1)
                   for j in range(coords[1] - self.diff, coords[1] + self.diff + 1)
                   if 0 <= i < self.n and 0 <= j < self.n])
        self.possible_squares = self.possible_squares.union(new)
        self.possible_squares.remove(coords)

    def remove(self, item: Tuple[int, int]) -> None:
        self.possible_squares.remove(item)
