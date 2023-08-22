from typing import List, Tuple


### The basic evaluation machanism is based on 2 principles:
# 1. The minimax is driven purely by the winning and losing positions, thus eval in [-1, 0, 1]
# 2. If the minimax returns more than one non-winning move line we will choose the best line by static_evaluator:
#   We check continuity of our pattern and check for newly created 2s, 3s and 5s (generally k, where k in [2,3,4]).
#   For each new k_th we add to static_evaluation 2**k.

def static_evaluation(board: List[List[int]], coords: Tuple[int, int]) -> int:
    n = len(board)
    x, y = coords
    # This will get the line of interest in any direction.
    def extract_line(dx: int, dy: int, length: int = 4) -> List[int]:
        line = []
        for step in range(-length, length + 1):  # We need to check up to 4 steps in each direction.
            nx, ny = x + step * dx, y + step * dy
            if 0 <= nx < n and 0 <= ny < n:
                line.append(board[nx][ny])
            else:
                line.append(0)  # Out of board, use None.
        return line

    def count_patterns(line: List[int], length: int) -> int:
        return sum(1 for i in range(len(line) - length + 1) if
                   all(cell == 1 for cell in line[i:i + length]) and (i == 0 or line[i - 1] != 1) and (
                               i + length == len(line) or line[i + length] != 1))

    # Check in all directions.
    directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]
    twos = threes = fours = 0
    for dx, dy in directions:
        line = extract_line(dx, dy)
        twos += count_patterns(line, 2)
        threes += count_patterns(line, 3)
        fours += count_patterns(line, 4)


    return twos * 2 ** 2 + threes * 2 ** 3 + fours * 2 ** 4


def winning_evaluation(board: List[List[int]], coords: Tuple[int, int]) -> bool:
    n = len(board)
    x, y = coords

    # Extract line of markers from the board given a direction and length.
    def extract_line(dx: int, dy: int, length: int) -> List[int]:
        return [board[x + i*dx][y + i*dy] if 0 <= x + i*dx < n and 0 <= y + i*dy < n else 0 for i in range(-length, length + 1)]

    # Check if there's a winning sequence in a given line.
    def has_five_in_row(line: List[int]) -> bool:
        return any(all(cell == 1 for cell in line[i:i + 5]) for i in range(len(line) - 4))

    # Check for a sequence of five in all directions.
    directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]
    for dx, dy in directions:
        line = extract_line(dx, dy, 4)  # 4 since we want to check a total of 9 cells
        if has_five_in_row(line):
            return True
    return False
