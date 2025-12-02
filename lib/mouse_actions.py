import pyautogui
import time

class MouseActions:
    def triple_click(self, x=None, y=None):
        if x and y:
            pyautogui.moveTo(x, y)
        for _ in range(3):
            pyautogui.click()
            time.sleep(0.1)
