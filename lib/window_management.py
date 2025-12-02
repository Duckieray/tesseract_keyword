import os
import subprocess
import time
import pygetwindow as gw

def nt_select_window(title, timeout=30):
    end = time.time() + timeout
    while time.time() < end:
        wins = gw.getWindowsWithTitle(title)
        if wins:
            try:
                wins[0].activate()
                return True
            except:
                time.sleep(0.5)
        time.sleep(1)
    raise RuntimeError(f"Window '{title}' not found")

def linux_select_window(title, timeout=30):
    end = time.time() + timeout
    while time.time() < end:
        out = subprocess.check_output(["wmctrl", "-l"]).decode()
        for line in out.splitlines():
            if title.lower() in line.lower():
                window_id = line.split()[0]
                subprocess.run(["wmctrl", "-ia", window_id])
                return True
        time.sleep(1)
    raise RuntimeError(f"Window '{title}' not found")
