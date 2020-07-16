from pyautogui import *

if sys.platform == "win32":
    platformModule = __import__("_pyautogui_win_direct_input")
