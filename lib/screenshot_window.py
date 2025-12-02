import subprocess
import pyautogui
import pygetwindow as gw

def win_screenshot_window(save_path):
    win = gw.getActiveWindow()
    x, y = win.left, win.top
    w, h = win.width, win.height
    shot = pyautogui.screenshot(region=(x, y, w, h))
    shot.save(save_path)

def linux_screenshot_window(save_path, title):
    out = subprocess.check_output(["xwininfo", "-name", title]).decode()
    x=y=w=h=None
    for line in out.splitlines():
        if "Absolute upper-left X:" in line: x = int(line.split(":")[1])
        if "Absolute upper-left Y:" in line: y = int(line.split(":")[1])
        if "Width:" in line: w = int(line.split(":")[1])
        if "Height:" in line: h = int(line.split(":")[1])

    shot = pyautogui.screenshot(region=(x,y,w,h))
    shot.save(save_path)
