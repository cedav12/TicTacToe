from game.engine.minimax_tree import Node, MinimaxTree, backpropagate
from game.engine.possible_squares import PossibleSquares
import time

from typing import List, Tuple, Dict


def minimax(coord: Tuple[int, int],
            board: Dict[str, List[List[int]]],
            possible_squares: PossibleSquares,
            depth: int) -> Tuple[int, int]:
    # Create Minimax_tree
    minmax = MinimaxTree(Node(coord))
    print(len(possible_squares.possible_squares))
    start = time.time()
    minmax.construct(minmax.head, board, possible_squares, 0, depth)
    print("--- %s seconds ---" % (time.time() - start))
    start = time.time()
    # 'Backpropagate' the minimax tree
    backpropagate(minmax.head, True)
    print("--- %s seconds ---" % (time.time() - start))
    return minmax.maximize(board[list(board.keys())[1]])

