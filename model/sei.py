import os
import re
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

from urllib.parse import urlparse, parse_qs

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
    #elements.clickElementBy(driver, 'sbmLogin')
    
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



def pesquisar(driver, list_document_sei):
    #for numero_sei in list_document_sei['SEI Number']:
    for index, row in list_document_sei.iterrows():
        numero_sei = row['SEI Number']
        elements.sendKeys(numero_sei, driver, 'txtPesquisaRapida')
        elements.sendKeys(Keys.ENTER, driver, 'txtPesquisaRapida')
        
        element = find_element_in_nested_iframes(driver, 'ifrVisualizacao', 'ifrArvoreHtml', 'divArvoreAcoes')
        
        list_document_sei.at[index, 'Validado'] = bool(element)
        
        if element:
            print('Disponível: '+ numero_sei + ' - :)')
            downloadFile(driver, str(numero_sei) +'_linha_'+ str(index))
        else:
            print('não dipsonível: '+ numero_sei)
            
    return list_document_sei

def findSubString(driver, page_source):
    # Define the substring to search for
    substring = "&infra_hash="

    # Find all occurrences of the substring and store their indices
    hashes = []
    start = 0

    while True:
        # Find the index of the next occurrence
        start_index = page_source.find(substring, start)
        if start_index == -1:
            break
        
        # Move start_index to the position after the found substring
        start_index += len(substring)
        
        # Find the closing character (in this case, the single quote or semicolon)
        end_index = page_source.find("'", start_index)
        
        # Extract the text between the start and end indices
        infra_hash = page_source[start_index:end_index]
        hashes.append(infra_hash)
        
        # Move to the next character after the current found index
        start = end_index
        
    return hashes

def downloadFile(driver, numero_sei_and_number_row):
    try:
        current_url = driver.current_url
        parsed_url = urlparse(current_url)
        query_params = parse_qs(parsed_url.query)

        id_protocolo = query_params.get('id_protocolo', [''])[0]
        infra_sistema = query_params.get('infra_sistema', [''])[0]
        infra_unidade_atual = query_params.get('infra_unidade_atual', [''])[0]
        infra_hash = query_params.get('infra_hash', [''])[0]
        
        # find_element_in_nested_iframes(driver, , 'ifrArvoreHtml', 'divArvoreAcoes')
        iframe = driver.find_element(By.ID, 'ifrVisualizacao')
        driver.switch_to.frame(iframe)
        
        # # ifrArvoreHtml é o texto dentro do documento do sei
        # iframe = driver.find_element(By.ID, 'ifrArvoreHtml')
        # driver.switch_to.frame(iframe)
        
        page_source = driver.page_source
        
        list_index = findSubString(driver, page_source)
        
        js_script = (
            f"window.open('controlador.php?acao=documento_imprimir_web&"
            f"acao_origem=arvore_visualizar&id_documento={id_protocolo}&"
            f"infra_sistema={infra_sistema}&infra_unidade_atual={infra_unidade_atual}&"
            f"infra_hash={infra_hash}');"
        )
        
        # ad5b085f3df4f8fb5beaa5c43f047bdadcf9c5da15ac315ddf8a17fe8b4496fa
        
        driver.execute_script(js_script)
        
        time.sleep(3)
        
        current_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
        
        full_file_path = f"{current_path}/files/{numero_sei_and_number_row}.pdf"

        driver.send_keys(full_file_path)
        time.sleep(1)
        driver.send_keys(Keys.RETURN)
    
    except (Exception) as e:
        print(e)
        
    
    

def executar(list_documento_sei):
    driver = None
    driver = logar(driver)
    
    if driver:
        pesquisar(driver, list_documento_sei)

# Exemplo de uso
# executar(['documento1', 'documento2'])
