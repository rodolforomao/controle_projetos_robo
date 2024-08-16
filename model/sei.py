import os
import sys
import time


import config.config as config

import model.elements as elements
import model.elements2 as elements2

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def logar(driver = None):
    
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--incognito')  # Opcional: abre em modo incógnito

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get('https://sei.dnit.gov.br/')
    
    text = config.sei_data['user']
    elements.sendKeys(text, driver, 'txtUsuario')
    text = config.sei_data['pwd']
    elements.sendKeys(text, driver, 'pwdSenha')
    elements.clickElementBy(driver, 'sbmLogin')
    
    if elements2.encontrar_elemento_agir(driver, 1, 5, 1, 'txtPesquisaRapida', '', elements.TYPE_METHOD_FIND_BY_ID
                                      , elements.TYPE_METHOD_ACTION_GET_ELEMENT, None):
        return driver

    return False


def find_element_in_nested_iframes(driver, outer_iframe_id, inner_iframe_id, element_id, retries=1, delay=1):
    sys.stderr = open(os.devnull, 'w')
    for attempt in range(retries):
        try:
            outer_iframe = driver.find_element(By.ID, outer_iframe_id)
            driver.switch_to.frame(outer_iframe)
            element = driver.find_element(By.ID, element_id)
            ## Achamos o primeiro elemento #############
            inner_iframe = driver.find_element(By.ID, inner_iframe_id)
            return inner_iframe
        
        except (NoSuchElementException, TimeoutException) as e:
            # Se não encontrar o iframe ou o elemento, aguardar e tentar novamente
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
        
        finally:
            # Sempre tente voltar ao conteúdo padrão antes da próxima tentativa
            driver.switch_to.default_content()
    
    # Se não encontrar o elemento após as tentativas
    #raise Exception(f"Element with ID '{element_id}' not found inside nested iframes after {retries} retries.")

    sys.stderr = sys.__stderr__



def pesquisar(driver, list_documento_sei):
    for numero_sei in list_documento_sei['SEI Number']:
        elements.sendKeys(numero_sei, driver, 'txtPesquisaRapida')
        elements.sendKeys(Keys.ENTER, driver, 'txtPesquisaRapida')
        
        element = find_element_in_nested_iframes(driver, 'ifrVisualizacao', 'ifrArvoreHtml', 'divArvoreAcoes')
        
        if element:
            print('Dipsonível: '+ numero_sei + ' - :)')
        else:
            print('não dipsonível: '+ numero_sei)
            
    return False


def executar(list_documento_sei):
    driver = None
    driver = logar(driver)
    
    if driver:
        pesquisar(driver, list_documento_sei)

# Exemplo de uso
# executar(['documento1', 'documento2'])
