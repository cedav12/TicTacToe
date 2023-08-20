import argparse
from game.game import TicTacToe


parser = argparse.ArgumentParser()

parser.add_argument("--engine", default=None, type=str,choices=["minimax_8"], help="engine algorithm, if None"
                                                                                   " initialize PVP game")
parser.add_argument("--symbols", default=("X", "O"), nargs="+", type=str)
parser.add_argument("--n", default=15, type=int, help="Define the size of the board, default 15x15.")


def main(args: argparse.Namespace) -> None:
    game = TicTacToe(args.n, symbols=args.symbols,  engine=args.engine)
    game.window.mainloop()


if __name__ == "__main__":
    # Parse arguments
    arg = parser.parse_args([] if "__file__" not in globals() else None)
    main(arg)