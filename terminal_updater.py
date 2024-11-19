#! .venv/bin/python3.13

from rich.table import Table
from rich.live import Live
from rich import box


def updateDisplay(board: list[list[str]], live: Live) -> None:
    digit_colors = ["cyan", "bright_magenta"]
    empty_color = "red"
    
    table = Table(title="Sudoku Solver",
                  show_header=False,
                  show_lines=True,
                  box=box.MINIMAL
                  )
    
    for i, row in enumerate(board):
        styles = []
        for j, item in enumerate(row):
            if item.isdigit():
                if j // 3 == 1:
                    styles.append(f"[{digit_colors[((i // 3) % 2 == 0)]}]{item}[/]")
                else:
                    styles.append(f"[{digit_colors[((i // 3) % 2 != 0)]}]{item}[/]")
            else:
                styles.append(f"[{empty_color}]{item}[/]")
        table.add_row(*styles)
    live.update(table)
    live.refresh()
