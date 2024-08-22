import time
import autoit
import win32gui
import win32con
import win32api

def find_window(title):
    return win32gui.FindWindow(None, title)

def click_button(hwnd, button_text):
    button_hwnd = win32gui.FindWindowEx(hwnd, 0, None, button_text)
    if button_hwnd == 0:
        raise Exception(f"Button with text '{button_text}' not found")
    win32gui.SendMessage(button_hwnd, win32con.BM_CLICK, 0, 0)

def set_text(hwnd, control_id, text):
    win32gui.SendMessage(hwnd, win32con.WM_SETTEXT, 0, text)

