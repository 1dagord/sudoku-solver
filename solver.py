#! .venv/bin/python3.13

from terminal_updater import updateDisplay


def isValid(board: list[list[int]], row: int, col: int, c: str) -> bool:
    """
        Check if row, column, or box contains duplicates
        :return: True if no dups found, False otherwise
    """
    for i in range(9):
        # checks row
        if board[row][i] == c:
            return False
        # checks column
        if board[i][col] == c:
            return False
        # checks box
        if board[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == c:
            return False

    return True


def solveSudoku(board: list[list[str]], live=None) -> bool:
    """
        Solves a 9x9 board of sudoku by way of backtracking
        implemented through recursion

        :param board: 9x9 nested list containing strings
                      of value 1-9 or "."
        :param live: instance of rich.live.Live()
                     that updates printed sudoku board
    """
    iter_count = 0
    for i in range(9):
        for j in range(9):
            
            # controls frequency of screen update
            # (speed of solver)
            iter_count += 1
            if iter_count == 20:
                updateDisplay(board, live)
                iter_count = 0
            
            if board[i][j] == ".":
                for c in "123456789":
                    if isValid(board, i, j, c):
                        board[i][j] = c
                        if solveSudoku(board, live):
                            return True
                        else:
                            board[i][j] = "."

                return False
    return True
