import time
import psutil
import subprocess
import pyautogui
import pygetwindow as gw


from selenium import webdriver

from selenium.common.exceptions import NoSuchWindowException, TimeoutException

def closeAllChromeInstances():
    subprocess.call("TASKKILL /f  /IM  CHROME.EXE")
    
    
