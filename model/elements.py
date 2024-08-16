import subprocess
import time
import controller.browser_util as browser_util

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import config

TYPE_METHOD_FIND_BY_ID = 0
TYPE_METHOD_FIND_BY_CLASSNAME = 1
TYPE_METHOD_FIND_BY_XPATH = 2
TYPE_METHOD_FIND_BY_PARTIALTEXTLINK = 3
TYPE_METHOD_FIND_BY_LINKTEXT = 4
TYPE_METHOD_FIND_BY_NAME = 5
TYPE_METHOD_FIND_BY_TAGNAME = 6
TYPE_METHOD_FIND_BY_NAME_CLICKABLE = 7

TYPE_METHOD_ACTION_CLICK = 0
TYPE_METHOD_ACTION_DOUBLECLICK = 1
TYPE_METHOD_ACTION_SET_VALUE = 2
TYPE_METHOD_ACTION_GET_ELEMENT = 3
TYPE_METHOD_ACTION_SEND_KEYS = 4

def checkElement( webdriver = None, idElement = None, findBy = 0, TypeElement = 0, timeout = None, chromeDriverPath = r"chromedriver.exe"):
    if webdriver is None:
        webdriver = browser_util.capturar_browser()
    exists = False
    # verifica elementos 
    if timeout is None:
        elemento = findElementBy(webdriver, idElement,findBy, TypeElement)
    else:
        elemento = findElementBy(webdriver, idElement,findBy, TypeElement,timeout)
    
    if findBy != 5:
        if elemento is not None:
            exists = True
    else:
        return elemento

    return exists


def clickElementBy(driver, idElement, findBy=0, TypeElement=0, webdriver = None, timeOut=10):
    element = findElementBy(driver, idElement, findBy, TypeElement, timeOut)
    if element:
        element.click()
    else:
        print(f"Element with id {idElement} not found")

def sendKeysAndClick(text ,driver, idElement_send, idElement_click, findBy = 0, TypeElement = 0, timeOut = 10):
    sendKeys(text , driver, idElement_send, findBy)
    element = findElementBy(driver, idElement_click, findBy, TypeElement, timeOut)
    if element is not None:
        element.click()
    

def sendKeys(text ,driver, idElement, findBy = 0, TypeElement = 0, timeOut = 10):
    element = findElementBy(driver, idElement, findBy, TypeElement, timeOut)
    if element is not None:
        element.send_keys(text)

def findElementBy(driver, idElement, findBy = 0, TypeElement = 0, timeOut = 10):
    
    element = None
    driver.implicitly_wait(timeOut * config.resolution_timeout)
    
    try:
        if findBy == 0:
            if TypeElement == 0:
                element = driver.find_element(By.ID, idElement)
            else:
                element = Select(driver.find_element(By.ID, idElement));
        else:
            if findBy == 1:
                if TypeElement == 0:
                    element = driver.find_element(By.NAME, idElement)
                else:
                    element = Select(driver.find_element(By.NAME, idElement));
            else:
                if findBy == 2:
                    if TypeElement == 0:
                        element = driver.find_element(By.XPATH, idElement)
                    else:
                        element = Select(driver.find_element(By.XPATH, idElement));
                else:
                    if findBy == 3:
                        if TypeElement == 0:
                            element = driver.find_element(By.PARTIAL_LINK_TEXT, idElement)
                        else:
                            element = Select(driver.find_element(By.PARTIAL_LINK_TEXT, idElement));
                    else:
                        if findBy == 4:
                            if TypeElement == 0:
                                element = driver.find_element(By.CLASS_NAME, idElement)
                            else:
                                element = Select(driver.find_element(By.CLASS_NAME, idElement));
                        else:
                            if findBy == 5:
                                if TypeElement == 0:
                                    element = driver.execute_script(idElement)
                                
    except:
        return element

    return element


def encontrar_elemento_agir(driver, wait_timeout_operation, number_attempts, sleep_timeout, elem_name, value, type_method_find, type_action, element_target):
    done = False
    repeat_operation = False
    number_attempts_done = 0
    
    wait = WebDriverWait(driver, wait_timeout_operation * config.resolution_timeout)
    
    if not elem_name or not driver:
        return False
    
    while not done and repeat_operation:
        try:
            number_attempts_done += 1
            
            if type_method_find == TYPE_METHOD_FIND_BY_ID:
                element_find = wait.until(EC.visibility_of_element_located((By.ID, elem_name)))
            elif type_method_find == TYPE_METHOD_FIND_BY_CLASSNAME:
                element_find = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, elem_name)))
            elif type_method_find == TYPE_METHOD_FIND_BY_XPATH:
                element_find = wait.until(EC.visibility_of_element_located((By.XPATH, elem_name)))
            elif type_method_find == TYPE_METHOD_FIND_BY_PARTIALTEXTLINK:
                element_find = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, elem_name)))
            elif type_method_find == TYPE_METHOD_FIND_BY_LINKTEXT:
                element_find = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, elem_name)))
            elif type_method_find == TYPE_METHOD_FIND_BY_NAME:
                element_find = wait.until(EC.visibility_of_element_located((By.NAME, elem_name)))
            elif type_method_find == TYPE_METHOD_FIND_BY_TAGNAME:
                element_find = wait.until(EC.visibility_of_element_located((By.TAG_NAME, elem_name)))
            elif type_method_find == TYPE_METHOD_FIND_BY_NAME_CLICKABLE:
                element_find = wait.until(EC.element_to_be_clickable((By.NAME, elem_name)))
            
            if type_action == TYPE_METHOD_ACTION_CLICK:
                if element_find:
                    element_find.click()
            elif type_action == TYPE_METHOD_ACTION_DOUBLECLICK:
                if element_find:
                    element_find.click()
                    element_find.click()
            elif type_action == TYPE_METHOD_ACTION_SET_VALUE:
                if element_find and value:
                    element_find.clear()
                    element_find.send_keys(value)
            elif type_action == TYPE_METHOD_ACTION_GET_ELEMENT:
                if element_find:
                    element_target = element_find
            elif type_action == TYPE_METHOD_ACTION_SEND_KEYS:
                if value:
                    element_find.send_keys(value)
            
            done = True
            repeat_operation = False
            
        except Exception as e:
            print(e)
        
        if sleep_timeout > 0 and repeat_operation:
            time.sleep(sleep_timeout * config.resolution_timeout)
        
        if number_attempts_done >= number_attempts:
            repeat_operation = False
    
    return done

def wait_iframe(driver, timeout = 0.25, watchdog = 4*10):
    count = 0
    script1 = "return document.querySelectorAll('iframe').length"
    script2 = """
            var divs = document.querySelectorAll('.Text_Note');
            var isVisible = false;
            divs.forEach(function(div) {
                if (div.textContent.includes('Aguarde enquanto')) {
                    if (window.getComputedStyle(div).display !== 'none') {
                        isVisible = true;
                    }
                }
            });
            return isVisible;
            """
    first_stage = False
    last_Stage = False
    while True:
        count += 1
        iframe_count = driver.execute_script(script1)
        if iframe_count > 0:
            mensagem_visivel = driver.execute_script(script2)   
            if str(mensagem_visivel) == 'True':
                first_stage = True
            if first_stage and str(mensagem_visivel) == 'False':
                break;
        time.sleep(timeout* config.resolution_timeout)
        if count >= watchdog:
            break;
