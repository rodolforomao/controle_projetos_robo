import os
import re
import sys
import time
import shutil
import requests
import certifi

import config.config_sei as config_sei
import config.config as config

import model.elements as elements
import model.elements2 as elements2
import model.excel as excel_class


import util.file as file
from csv import excel

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from urllib.parse import urlparse, parse_qs

import model.autoit as autoit

def logar(driver = None):
    
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--incognito') 
    
    default_download_directory = os.path.join(os.path.expanduser("~"), "Downloads")

    chrome_prefs = {
    'printing.print_preview_sticky_settings.appState': '{"recentDestinations":[{"id":"Save as PDF","origin":"local","account":"","name":"Salvar como PDF"}],"selectedDestinationId":"Save as PDF","version":2}',
    "download.default_directory": default_download_directory,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True,
    "download.directory_upgrade": True,

    }

    chrome_options.add_experimental_option('prefs', chrome_prefs)
    chrome_options.add_argument('--kiosk-printing')

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get('https://sei.dnit.gov.br/')
    
    text = config_sei.sei_data['user']
    elements.sendKeys(text, driver, 'txtUsuario')
    text = config_sei.sei_data['pwd']
    elements.sendKeys(text, driver, 'pwdSenha')
    
    if elements2.encontrar_elemento_agir(driver, 1, 5, 1, 'sbmLogin', '', elements2.TYPE_METHOD_FIND_BY_ID
                                      , elements2.TYPE_METHOD_ACTION_CLICK, None):
        return driver

    return False


def find_element_in_nested_iframes_and_action(driver, outer_iframe_id, inner_iframe_id, element_id, element_xpath, retries=1, delay=1):
    sys.stderr = open(os.devnull, 'w')
    for attempt in range(retries):
        try:
            outer_iframe = driver.find_element(By.ID, outer_iframe_id)
            driver.switch_to.frame(outer_iframe)
            element = driver.find_element(By.ID, element_id)
            
            inner_iframe = driver.find_element(By.ID, inner_iframe_id)
            driver.switch_to.frame(inner_iframe)
            elements.encontrar_elemento_agir(driver, 1, 5, 1, element_xpath,'',elements.TYPE_METHOD_FIND_BY_ID, elements.TYPE_METHOD_ACTION_CLICK, None)
            return bool(elements)
        
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
        
        finally:
            driver.switch_to.default_content()
    
    sys.stderr = sys.__stderr__
    
def find_element_in_nested_iframes(driver, outer_iframe_id, inner_iframe_id = None, element_id = None, retries=1, delay=1):
    sys.stderr = open(os.devnull, 'w')
    for attempt in range(retries):
        try:
            outer_iframe = driver.find_element(By.ID, outer_iframe_id)
            driver.switch_to.frame(outer_iframe)
            if element_id is None:
                return outer_iframe
            else:
                if element_id != '':
                    element = driver.find_element(By.ID, element_id)
            inner_iframe = driver.find_element(By.ID, inner_iframe_id)
            return inner_iframe
        
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
        
        finally:
            driver.switch_to.default_content()
    

    sys.stderr = sys.__stderr__



def pesquisar(driver, list_document_sei):
    validation_list = {}
    
    for index, row in list_document_sei.iterrows():
        numero_sei = row['SEI Number']
        elements.sendKeys(numero_sei, driver, 'txtPesquisaRapida')
        elements.sendKeys(Keys.ENTER, driver, 'txtPesquisaRapida')
        element = find_element_in_nested_iframes(driver, 'ifrVisualizacao', 'ifrArvoreHtml', 'divArvoreAcoes')
        list_document_sei.at[index, 'Validado'] = bool(element)

        if element:
            print('Disponível: '+ numero_sei + ' - :)')
            validation_list[index] = True
            if config.DOWNLOAD_sei:
                name_file = numero_sei + '_' + str(index)
                downloadFile(driver, name_file)
        else:
            validation_list[index] = False
            print('não dipsonível: '+ numero_sei)
    
    if config.VALIDACAO_SEI:
        excel_class.realizar_validacao_excel(list_document_sei, validation_list)
    
    return list_document_sei

def findSubString(driver, page_source):
    substring = "&infra_hash="

    hashes = []
    start = 0

    while True:
        start_index = page_source.find(substring, start)
        if start_index == -1:
            break
        
        start_index += len(substring)
        
        end_index = page_source.find("'", start_index)
        
        infra_hash = page_source[start_index:end_index]
        hashes.append(infra_hash)
        
        start = end_index
        
    return hashes

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def downloadFile(driver, numero_sei_and_number_row):
    max_retries = 3
    retry_count = 0

    download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    target_dir = './files/sei_downloaded'
    os.makedirs(target_dir, exist_ok=True)

    while retry_count < max_retries:
        try:
            existing_files = set(os.listdir(download_dir))
            
            iframe = find_element_in_nested_iframes(driver, 'ifrVisualizacao')
            if iframe is not None:
                driver.switch_to.frame(iframe)
                        
            if click_printer(driver):
            
                timeout = 30
                start_time = time.time()

                while True:
                    new_files = set(os.listdir(download_dir)) - existing_files
                    download_finished = checkDownloadFinished(new_files)
                    if new_files and download_finished:
                        new_file_name = new_files.pop() 
                        downloaded_file_path = os.path.join(download_dir, new_file_name)
                        try:
                            target_path = os.path.join(target_dir, new_file_name)
                            file.move(downloaded_file_path, target_path)
                            break
                        except Exception as e:
                            print(f"Attempt to move file again failed: {e}")
                    
                    if time.time() - start_time > timeout:
                        raise Exception("File download timed out.")
                
                return True
        
        except Exception as e:
            print(f"Attempt {retry_count + 1} failed: {e}")
            retry_count += 1
            time.sleep(2)
        finally:
            driver.switch_to.default_content()
        
        return False

def checkDownloadFinished(file):
    return '.crdownload' not in str(file) and '.tmp' not in str(file) 

def executar(list_documento_sei):
    driver = None
    driver = logar(driver)
    
    if driver:
        pesquisar(driver, list_documento_sei)

def click_printer(driver):
    element = None
    try:
        element = WebDriverWait(driver, 1, poll_frequency=0.2).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick, 'documento_imprimir_web') and @class='botaoSEI']/img[@class='infraCorBarraSistema']"))
        )
        element.click()
        return True
    except Exception as e:
        print(f"Procura 1 - failed")
                
    if element is None:
        try:
            driver.switch_to.default_content()
            print(f"Procura 3 - Embedded")
            iframe = driver.find_element(By.ID, 'ifrVisualizacao')
            if iframe is not None:
                driver.switch_to.frame(iframe)
                
            element = driver.find_element(By.ID, 'ifrArvoreHtml')
            if element is not None:
                pdf_url = element.get_attribute('src')
                
                driver.get(pdf_url)
                
                max_wait_time = 5
                elapsed_time = 0
                interval = 0.5 

                while elapsed_time < max_wait_time:
                    try:
                        save_as_hwnd = autoit.find_window("Salvar como")
                    except ValueError as e:
                        print(f'ValueError: {e}')
                    except autoit.AutoItError as e:
                        print(f'AutoItError: {e}')
                    except Exception as e:
                        print(f'Exception: {e}')
                        
                    if save_as_hwnd != 0:
                        break
                    else:
                        print('procurando autoit')
                    
                    time.sleep(interval)
                    elapsed_time += interval

                if save_as_hwnd:
                    tag = 'Sa&lvar'
                    autoit.find_window(tag)
                    autoit.click_button(save_as_hwnd, tag)
            
                return True
            
        except Exception as e:
            print(f"Procura 3 - failed - {e}")

    if element is None:
        try:
                element = WebDriverWait(driver, 1, poll_frequency=0.2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.botaoSEI[onclick*='documento_imprimir_web'] > img.infraCorBarraSistema"))
                )
                element.click()
            
                return True
            
        except Exception as e:
            print(f"Procura 2 - failed")
            
    return False


