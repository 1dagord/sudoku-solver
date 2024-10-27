#! .venv/bin/python3.13

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
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
    
    # check if most current board already obtained
    with open("daily_board.txt", "r") as file:
        if line := file.readline():
            board_date = int(line)
            
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
    options.add_argument("--headless")

    driver = webdriver.Safari(options=options)
    driver.minimize_window()

    driver.get("https://www.dailysudoku.com/sudoku/play.shtml?today=1")
    time.sleep(10)

    try:
        squares = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//input[@onfocus]"
                )
            )
        )
    except TimeoutException:
        print("Could not get daily board")
        return board

    for j in range(9):
        row = []
        for i in range(9):
            row.append(squares[i + 9 * j].get_attribute("value"))
        row = (str(row).replace(" ", "")).replace("''", "'.'")
        board.append(eval(row))
        
    print("Daily Sudoku Board Obtained!")
    driver.quit()

    # writes board to file for faster access
    with open("daily_board.txt", "w") as file:
        file.write(str(current_date))
        for row in board:
            file.write("\n"+str(row))


    return board
