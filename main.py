import cv2 as cv
import numpy as np
import pygetwindow as gw
import pyautogui
import time
import random


def hamster(titles: list, hold: float, circle: int):
    for title in titles:
        if gw.getWindowsWithTitle(title):
            windows = gw.getWindowsWithTitle(title)[0]
            screenshot = pyautogui.screenshot(region=(windows.left, windows.top, windows.width, windows.height))
            screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2GRAY)
            screenshot = cv.Canny(screenshot, 100, 100)
            loc = get_loc_hamster(screenshot, hold)
            if number_is_true(screenshot, hold):
                print(f"Изображение найдено на координатах: {windows.left}, {windows.top}")
                loc = get_loc_hamster(screenshot, hold)
                for _ in range(circle):
                    per = random.randint(0, 100)
                    pyautogui.click((windows.left + loc[1][0] + 150 + per, loc[0][0] + windows.top + 150 + per))
                    interval = random.uniform(0.1, 0.5)
                    time.sleep(interval)
            else:
                print("Изображение не найдено на экране")
                time.sleep(0.5)
            time.sleep(0.5)


def number_is_true(screenshot, hold) -> bool:
    img = cv.imread('./img/number.png')
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.Canny(img, 100, 100)
    result = cv.matchTemplate(screenshot, img, cv.TM_CCOEFF_NORMED)
    threshold = hold
    loc = np.where(result >= threshold)
    if len(loc[0]) == 0:
        return False
    return True


def get_loc_hamster(screenshot, hold):
    img = cv.imread('./img/target.png')
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.Canny(img, 100, 100)
    result = cv.matchTemplate(screenshot, img, cv.TM_CCOEFF_NORMED)
    return np.where(result >= hold)


titles = input("Введите название окна, через запятую: ").split()
hold = float(input("Частота поиска 0.5 - 1.0: "))
circle = int(input("Количество кликов: "))
while True:
    hamster(titles, hold, circle)
    if input("Продолжить? (y/n) ").lower() == 'n':
        break

