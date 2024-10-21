#! .venv/bin/python3.13

from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium import webdriver

import datetime
import time


def getSudokuBoard() -> list[list[int]]:
    """
        Loads in sudoku board from Marty's Daily Sudoku website

        :return: 9x9 sudoku board to be solved
    """
    board = []
    current_time = datetime.datetime.now()
    current_date = int(str(current_time.year) +
                       str(current_time.month) +
                       str(current_time.day)
                       )
    
    with open("daily_board.txt", "r") as file:
        board_date = int(file.readline())
        
        if current_date <= board_date:
            for row in file:
                line = eval(row.replace("''", "'.'"))
                board.append(line)
            return board
          
    print("Getting Daily Sudoku Board...")
    
    # start driver
    options = webdriver.SafariOptions()

    ua = UserAgent(browsers=["safari"])
    options.add_argument(f"user-agent={ua.random}")
    options.add_argument("--incognito")
    options.add_argument("--headless=new")

    driver = webdriver.Safari(options=options)
    driver.minimize_window()

    driver.get("https://www.dailysudoku.com/sudoku/play.shtml?today=1")
    time.sleep(10)

    squares = driver.find_elements(
        By.XPATH,
        "//input[@onfocus]"
    )

    for j in range(9):
        row = []
        for i in range(9):
            row.append(squares[i + 9 * j].get_attribute("value"))
        board.append(row)
        
    print("Daily Sudoku Board Obtained!")
    driver.quit()

    return board
