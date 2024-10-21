#! .venv/bin/python3.13

from rich.table import Table
from rich.live import Live
from rich import box


def updateDisplay(board: list[list[str]], live: Live) -> None:
    digit_color = "cyan"
    empty_color = "red"
    
    table = Table(title="Sudoku Solver",
                  show_header=False,
                  show_lines=True,
                  box=box.MINIMAL
                  )
    
    for row in board:
        styles = []
        for item in row:
            if item.isdigit():
                styles.append(f"[{digit_color}]{item}[/]")
            else:
                styles.append(f"[{empty_color}]{item}[/]")
        table.add_row(*styles)
    live.update(table)
    live.refresh()
