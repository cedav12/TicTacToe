import tkinter as tk
from tkinter import messagebox
import tkinter.font as fnt
import random
from typing import List, Tuple, Callable


class TicTacToe:
    def __init__(self, n: int, symbols: Tuple[str, str] = ("X", "O"),
                 engine: Callable[[List[List[str]]], Tuple[int, int]] | None = None):
        self.n = n
        #Player symbols
        self.X, self.O = symbols
        # Initialize tkinter window.
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        # Initialize backend board with empty strings.
        self.board: List[List[str]] = [['' for _ in range(n)] for _ in range(n)]
        self.buttons = [[None for _ in range(n)] for _ in range(n)]
        # Variable indicating who is on move.
        self.current_player = self.X
        # Initialize engine
        self.engine = engine

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
        if self.board[row][col] == '':
            # Add move.
            self.board[row][col] = self.current_player
            self.buttons[row][col]['text'] = self.current_player
            self.buttons[row][col]["fg"] = "blue" if self.current_player == self.X else "red"
            # Check whather the game is over.
            if self.is_game_over(row, col):
                messagebox.showinfo("Game Over", f"Player {self.current_player} Wins!")
                self.window.quit()
            else:

                if self.engine:
                    self.current_player = self.O
                    self.computer_move(self.engine)
                else:
                    self.current_player = 'O' if self.current_player == 'X' else 'X'
        else:
            messagebox.showinfo("Invalid Move", "The selected cell is not empty!")

    def computer_move(self, engine: Callable[[List[List[str]]], Tuple[int, int]]) -> None:
        while True:
            row, col = engine(self.board)
            row = random.randint(0, self.n - 1)
            col = random.randint(0, self.n - 1)
            if self.board[row][col] == '':
                self.board[row][col] = self.current_player
                self.buttons[row][col]['text'] = self.current_player
                break
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

    """def check_line(self, row, col, dx, dy):
        count = 0
        for d in [-4, -3, -2, -1, 0]:
            r, c = row + d * dx, col + d * dy
            if not (0 <= r < self.n and 0 <= c < self.n) or self.board[r][c] != self.board[row][col]:
                count = 0
            else:
                count += 1
            if count == 5:
                return True
        return False"""

    def check_line(self, row: int, col: int, dx: int, dy: int) -> bool:
        """Check possible winning combination from given orientation."""
        for start in [-4, -3, -2, -1, 0]:
            valid = True
            for i in range(5):
                r, c = row + (start+i) * dx, col + (start+i) * dy
                if not (0 <= r < self.n and 0 <= c < self.n) or self.board[r][c] != self.board[row][col]:
                    valid = False
                    break
            if valid:
                return True
        return False

if __name__ == '__main__':
    game = TicTacToe(15)
    game.window.mainloop()
