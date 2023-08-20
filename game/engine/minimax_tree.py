from typing import Tuple, List


class Node:
    def __init__(self, move: Tuple[int, int], value: int = None, children: List | None = None):
        self.value = value
        self.children = children or []
        # the last move, which defines the position
        self.move = move

    def maximize(self) -> None:
        """Maximize value of the Node children"""
        if self.children:
            max = self.children[0].value
            for i in range(1, len(self.children)):
                val = self.children[i].value
                if val > max:
                    max = val
            return max
        return None

    def minimize(self) -> None:
        """minimize value of the Node children"""
        if self.children:
            min = self.children[0].value
            for i in range(1, len(self.children)):
                val = self.children[i].value
                if val < min:
                    min = val
            return min
        return None


class MinimaxTree:
    def __init__(self, head: Node = None):
        self.head = head
