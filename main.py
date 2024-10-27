#! .venv/bin/python3.13

from rich.table import Table
from rich.live import Live
from rich import box

from webscraper import getSudokuBoard
from solver import solveSudoku

import sys


def main() -> None:
    table = Table(title="Sudoku Solver",
                  show_header=False,
                  show_lines=True,
                  box=box.MINIMAL
                  )
    
    with Live(table) as live:

        for row in (board := getSudokuBoard()):
            table.add_row(*row)

        try:
            solveSudoku(board, live)
        except KeyboardInterrupt:
            print("Solver Interrupted!")
            sys.exit(0)


if __name__ == "__main__":
    main()
