import os
import shutil

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def verify_update_webdriver():
    options = webdriver.ChromeOptions()
    driver_path = ChromeDriverManager().install()
    driver_directory = os.path.dirname(driver_path)
    destination_path = os.path.join('lib', 'chromedriver.exe')
    shutil.copy(driver_path, destination_path)
