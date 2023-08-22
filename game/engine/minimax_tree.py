from typing import Tuple, List, Dict
from game.engine.possible_squares import PossibleSquares
from game.engine.evaluation import static_evaluation, winning_evaluation


class Node:
    def __init__(self, move: Tuple[int, int], parent = None, value: int = None, children: List | None = None,
                 depth: int = 0):
        self.value = value
        self.children = children or []
        self.parent = parent
        # the last move, which defines the position
        self.move = move
        self.depth = depth


class MinimaxTree:
    def __init__(self, head: Node = None):
        self.head = head

    def construct(self, node: Node,
                  board: Dict[str, List[List[int]]],
                  possible_squares: PossibleSquares,
                  depth: int,
                  max_depth: int) -> None:
        # Check if we reached the max depth
        if node.depth == max_depth:
            return

        # Determine the current player based on the depth
        current_player = list(board.keys())[(node.depth + 1) % 2]
        opponent = list(board.keys())[node.depth % 2]


        # Get possible moves from the current board state
        moves = possible_squares.possible_squares.copy()

        for move in moves:
            # Create new boards from the previous state
            new_board = {player: [row.copy() for row in board] for player, board in board.items()}
            # Update the board for the current player
            if new_board[opponent][move[0]][move[1]] != 1 and new_board[current_player][move[0]][move[1]] != 1:
                new_board[current_player][move[0]][move[1]] = 1
                # Create child node and link to parent (current node)
                child_node = Node(move, depth=node.depth + 1)

                node.children.append(child_node)
                winning = winning_evaluation(new_board[current_player], move)
                if winning:
                    child_node.value = 1 if current_player == list(board.keys())[1] else -1
                    break
                else:
                    # Recurse to construct the subtree
                    child_node.value = 0
                    # Create a new possible_squares object.
                    new_possible_squares = PossibleSquares(possible_squares.possible_squares, possible_squares.n,
                                                           diff=possible_squares.diff)
                    new_possible_squares.update(move)
                    self.construct(child_node, new_board, new_possible_squares, depth, max_depth)
            else:
                possible_squares.remove(move)

        return

    def maximize(self, board: List[List[int]]) -> Tuple[int, int]:
        """Returns best move"""
        maximizer = self.head.value
        # If the possition is winning it is irrelevant which winning combination we play.
        if maximizer == 1:
            # Find the node with value 1, i.e. winning node.
            for i in range(len(self.head.children)):
                p = self.head.children[i]
                if p.value == maximizer:
                    return p.move
        # Otherwise if the position is not winning, we will choose the best move, from our possibilities by using
        # static_evaluator.
        if maximizer == 0:
            moves = [p for p in self.head.children if p.value == maximizer]
        else:
            moves = [p for p in self.head.children]
        if len(moves) > 1:
            max_eval = -1
            candidate = None
            for move in moves:
                move = move.move
                provisory_board = [row.copy() for row in board]
                row, col = move
                provisory_board[row][col] = 1
                eval = static_evaluation(provisory_board, move)
                if eval > max_eval:
                    candidate = move
                    max_eval = eval
            return candidate
        else:
            return moves[0].move

    def update(self):
        """Function which upgrade already created tree, which anables us to cache the tree."""
        raise NotImplementedError


def backpropagate(node: Node, is_maximizing: bool) -> int:
    """evaluate each node according to  min/max value of its children"""
    # If the node is a leaf, return its value
    if not node.children:
        return node.value
    # For a maximizing node
    if is_maximizing:
        child_values = [backpropagate(child, False) for child in node.children]
        # Check if any child has a winning move
        if 1 in child_values:
            node.value = 1
            return 1
        elif 0 in child_values:
            node.value = 0
            return 0
        # If all children have a losing move
        else:
            node.value = -1
            return -1
    # For a minimizing node
    else:
        child_values = [backpropagate(child, True) for child in node.children]
        # Check if any child has a losing move (which is a win for minimizer)
        if -1 in child_values:
            node.value = -1
            return -1

        elif 0 in child_values:
            node.value = 0
            return 0
        # If all children have a winning move for maximizer (which is a lose for minimizer)
        else:
            node.value = 1
            return 1
