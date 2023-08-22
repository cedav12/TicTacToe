import tkinter as tk
from tkinter import messagebox
import tkinter.font as fnt
from typing import List, Tuple, Dict
from game.engine.minimax_config import DEPTH, DIST
from game.engine.possible_squares import PossibleSquares
from game.engine.minimax import minimax


class TicTacToe:
    def __init__(self, n: int, symbols: Tuple[str, str] = ("X", "O"),
                 engine: bool = False):
        self.n = n
        #Player symbols
        self.X, self.O = symbols
        # Initialize tkinter window.
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        # Initialize backend board as separate board for each player with 1 as nonempty square and 0 otherwise.
        self.board: Dict[str, List[List[int]]] = {player: [[0 for _ in range(n)] for _ in range(n)]
                                                  for player in [self.X, self.O]}
        self.buttons = [[None for _ in range(n)] for _ in range(n)]
        # Variable indicating who is on move.
        self.current_player = self.X
        # Initialize engine
        self.engine = engine
        self.last_move: Tuple[int, int] | None = None
        self.possible_squares = PossibleSquares(n=self.n, diff=DIST)

        for i in range(n):
            for j in range(n):
                self.buttons[i][j] = tk.Button(self.window,
                                               # buttons are empty.
                                               text='',
                                               # when button is clicked the make_move method is called.
                                               command=lambda row=i, col=j: self.make_move(row, col),
                                               height=2,
                                               width=5,
                                               bg="lightblue",
                                               font=fnt.Font(size=13, weight="bold"),
                                               )
                # Buttons are placed into grid scheme.
                self.buttons[i][j].grid(row=i, column=j)

    def make_move(self, row: int, col: int) -> None:
        """Move method."""
        # check whather the chosen square is free.
        if self.board[self.current_player][row][col] == 0:
            # Add move.
            self.board[self.current_player][row][col] = 1
            self.last_move = (row, col)
            self.possible_squares.update(self.last_move)

            self.buttons[row][col]['text'] = self.current_player
            self.buttons[row][col]["fg"] = "blue" if self.current_player == self.X else "red"
            # Check whather the game is over.
            if self.is_game_over(row, col):
                messagebox.showinfo("Game Over", f"Player {self.current_player} Wins!")
                self.window.quit()
            else:
                if self.engine:
                    self.current_player = self.O
                    self.window.after(100, self.computer_move)
                    #self.computer_move()
                else:
                    self.current_player = 'O' if self.current_player == 'X' else 'X'
        else:
            messagebox.showinfo("Invalid Move", "The selected cell is not empty!")

    def computer_move(self) -> None:
        row, col = minimax(self.last_move, self.board, self.possible_squares, DEPTH)
        self.board[self.current_player][row][col] = 1
        self.possible_squares.update((row, col))
        self.buttons[row][col]['text'] = self.current_player
        self.buttons[row][col]["fg"] = "blue" if self.current_player == self.X else "red"
        if self.is_game_over(row, col):
            messagebox.showinfo("Game Over", f"Computer Wins!")
            self.window.quit()
        else:
            self.current_player = 'X'

    def is_game_over(self, row: int, col: int) -> bool:
        """Check all 4 possible orientations of possible winning combination."""
        if self.check_line(row, col, 0, 1) or self.check_line(row, col, 1, 0) or\
                self.check_line(row, col, 1, 1) or self.check_line(row, col, -1, 1):
            return True
        return False

    def check_line(self, row: int, col: int, dx: int, dy: int) -> bool:
        """Check possible winning combination from given orientation."""
        for start in [-4, -3, -2, -1, 0]:
            valid = True
            for i in range(5):
                r, c = row + (start+i) * dx, col + (start+i) * dy
                if not (0 <= r < self.n and 0 <= c < self.n) or self.board[self.current_player][r][c] != 1:
                    valid = False
                    break
            if valid:
                return True
        return False
