# src/automation/desktop.py
import pyautogui, subprocess, time
from typing import Dict

class DesktopAutomator:
    def __init__(self):
        self.app_processes: Dict[str, subprocess.Popen] = {}
        pyautogui.FAILSAFE = False

    def open_app(self, app_name: str = None, app: str = None, application: str = None) -> bool:
        name_to_open = app_name or app or application
        if not name_to_open: raise ValueError("No app name provided.")
        name_to_open = name_to_open.lower()
        self.app_processes[name_to_open] = subprocess.Popen(name_to_open)
        time.sleep(2)
        return True

    def keyboard_input(self, text: str):
        pyautogui.write(text, interval=0.01)

    # Defensive alias for a common AI hallucination
    def type(self, text: str):
        self.keyboard_input(text)

    def mouse_click(self, x: int, y: int, button: str = 'left'):
        pyautogui.click(x, y, button=button)

    def close(self):
        for proc in self.app_processes.values():
            if proc.poll() is None:
                proc.terminate()