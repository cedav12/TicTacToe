from typing import Tuple


class PossibleSquares:
    """Object which stores possible moves, which will be processed in minimax calculation."""

    def __init__(self, possible: set | None = None, n: int = 15, diff: int = 2):
        self.possible_squares: set = possible if possible else set()
        # Size of the board
        self.n = n
        # As possible move will be consider move with distance from nearest nonempty square <= 'diff'.
        self.diff = diff

    def update(self, coords: Tuple[int, int], opt_dist: int | None = None):
        if opt_dist:
            dist = self.diff + opt_dist
        else:
            dist = self.diff
        new = set([(i, j) for i in range(coords[0] - dist, coords[0] + dist + 1)
                   for j in range(coords[1] - dist, coords[1] + dist + 1)
                   if 0 <= i < self.n and 0 <= j < self.n])
        self.possible_squares = self.possible_squares.union(new)
        # Remove the latest move, since the square is now nonempty.
        self.possible_squares.remove(coords)

    def remove(self, item: Tuple[int, int]) -> None:
        self.possible_squares.remove(item)
