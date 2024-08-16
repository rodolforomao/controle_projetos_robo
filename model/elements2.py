from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from config import config
import time

TYPE_METHOD_FIND_BY_ID = 1
TYPE_METHOD_FIND_BY_CLASSNAME = 2
TYPE_METHOD_FIND_BY_XPATH = 3
TYPE_METHOD_FIND_BY_PARTIALTEXTLINK = 4
TYPE_METHOD_FIND_BY_LINKTEXT = 5
TYPE_METHOD_FIND_BY_NAME = 6
TYPE_METHOD_FIND_BY_NAME_CLICKABLE = 7
TYPE_METHOD_FIND_BY_TAGNAME = 8
TYPE_METHOD_FIND_BY_ID_GETATTRIBUTE = 9

TYPE_METHOD_ACTION_NONE = 1
TYPE_METHOD_ACTION_CLICK = 2
TYPE_METHOD_ACTION_SET_VALUE = 3
TYPE_METHOD_ACTION_GET_ELEMENT = 4
TYPE_METHOD_ACTION_SEND_KEYS = 5
TYPE_METHOD_ACTION_DOUBLECLICK = 6

def encontrar_elemento_agir(driver, wait_timeout_operation, number_attempts, sleep_timeout, elem_name, value, type_method_find, type_action, element_target):
    done = False
    repeat_operation = False
    number_attempts = 0

    wait = WebDriverWait(driver, wait_timeout_operation * config.resolution_timeout)

    if not elem_name or not driver:
        return False

    while not done:
        element_finded = None

        try:
            number_attempts += 1

            if type_method_find == TYPE_METHOD_FIND_BY_ID:
                element_finded = wait.until(EC.visibility_of_element_located((By.ID, elem_name)))
            elif type_method_find == TYPE_METHOD_FIND_BY_CLASSNAME:
                element_finded = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, elem_name)))
            elif type_method_find == TYPE_METHOD_FIND_BY_XPATH:
                element_finded = wait.until(EC.visibility_of_element_located((By.XPATH, elem_name)))
            elif type_method_find == TYPE_METHOD_FIND_BY_PARTIALTEXTLINK:
                element_finded = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, elem_name)))
            elif type_method_find == TYPE_METHOD_FIND_BY_LINKTEXT:
                element_finded = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, elem_name)))
            elif type_method_find == TYPE_METHOD_FIND_BY_NAME:
                element_finded = wait.until(EC.visibility_of_element_located((By.NAME, elem_name)))
            elif type_method_find == TYPE_METHOD_FIND_BY_TAGNAME:
                element_finded = wait.until(EC.visibility_of_element_located((By.TAG_NAME, elem_name)))
            elif type_method_find == TYPE_METHOD_FIND_BY_NAME_CLICKABLE:
                element_finded = wait.until(EC.element_to_be_clickable((By.NAME, elem_name)))

            if type_action == TYPE_METHOD_ACTION_CLICK:
                if element_finded:
                    element_finded.click()
            elif type_action == TYPE_METHOD_ACTION_DOUBLECLICK:
                if element_finded:
                    element_finded.click()
                    element_finded.click()
            elif type_action == TYPE_METHOD_ACTION_SET_VALUE:
                if element_finded and value:
                    element_finded.clear()
                    element_finded.send_keys(value)
            elif type_action == TYPE_METHOD_ACTION_GET_ELEMENT:
                if element_finded:
                    element_target.clear()
                    element_target.append(element_finded)
            elif type_action == TYPE_METHOD_ACTION_SEND_KEYS:
                if value:
                    element_finded.send_keys(value)

            repeat_operation = False
            done = True

        except NoSuchElementException:
            repeat_operation = True
        except ElementNotInteractableException:
            repeat_operation = True

        if sleep_timeout > 0 and repeat_operation:
            time.sleep(sleep_timeout* config.resolution_timeout)

        if number_attempts >= number_attempts:
            repeat_operation = False

    return done
