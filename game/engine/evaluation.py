from typing import List, Tuple


### The basic evaluation machanism is based on 2 principles:
# 1. The side which connects 5 or more symbols wins, thus the evaluation is +/- 1.
# 2. For each move, assign a new valuation position according to how many symbols the move directly
#   connects (in a row/column/diagonal), by adding +/- 2**n for n connected symbols to the current evaluation.

def static_evaluation(board: List[List[int]], coords: Tuple[int, int]) -> Tuple[bool, int]:
    n = len(board)
    x, y = coords
    # This will get the line of interest in any direction.
    def extract_line(dx: int, dy: int, length: int = 5) -> List[int]:
        line = []
        for step in range(-length, length + 1):  # We need to check up to 4 steps in each direction.
            nx, ny = x + step * dx, y + step * dy
            if 0 <= nx < n and 0 <= ny < n:
                line.append(board[nx][ny])
            else:
                line.append(None)  # Out of board, use None.
        return line

    def count_patterns(line: List[int], length: int) -> int:
        return sum(1 for i in range(len(line) - length + 1) if
                   all(cell == 1 for cell in line[i:i + length]) and (i == 0 or line[i - 1] != 1) and (
                               i + length == len(line) or line[i + length] != 1))

    # Check in all directions.
    directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]
    twos = threes = fours = five = 0
    for dx, dy in directions:
        line_five = extract_line(dx, dy)
        line = line_five[1:-1]
        twos += count_patterns(line, 2)
        threes += count_patterns(line, 3)
        fours += count_patterns(line, 4)
        five += count_patterns(line_five, 5)


    return True if five != 0 else False, twos * 2 ** 2 + threes * 2 ** 3 + fours * 2 ** 4


if __name__ == "__main__":
    board = [[0 for _ in range(15)] for _ in range(15)]
    board[7][7] = 1
    board[8][8] = 1
    board[9][9] = 1
    board[10][10] = 1
    #board[11][11] = 1# Pretend player 1 made a move in the center
    print(static_evaluation(board, (7,7)))