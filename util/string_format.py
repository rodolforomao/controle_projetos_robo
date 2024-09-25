import re
import math
import unicodedata
from fuzzywuzzy import fuzz

import util.string_format as string_format

def normalize_text(name):
    # Remove spaces, convert to lowercase, and remove accents
    name = name.strip().replace(" ", "").lower()
    name = remove_accents(name)
    return name

def remove_accents(input_str):
    # Function to remove accents from characters
    import unicodedata
    return ''.join(
        (c for c in unicodedata.normalize('NFD', input_str) if unicodedata.category(c) != 'Mn')
    )


def normalizar_texto(texto):
    if texto is not None and len(texto) > 0:
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
        texto = re.sub(r'[^a-zA-Z0-9]', '', texto).lower()
        return texto
    return ''

def normalizar_nome_arquivo(texto):
    if texto is not None and len(texto) > 0:
        texto = texto.replace(" ", "_").replace("/", "_").replace("\\", "_")
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
        texto = re.sub(r'[^a-zA-Z0-9_.]', '', texto).lower()
        return texto
    return ''

def comparar_strings(string1, string2, limiar=80, normalizar = False):
    if normalizar:
        string1 = normalizar_texto(string1)
        string2 = normalizar_texto(string2)
    similaridade = fuzz.ratio(string1, string2)
    return similaridade >= limiar


def get_item(value, dados_banco, column, get_one = True, precisao  = 80):
    resultados = []
    
    if value is not None:
        termos_normalizados = normalizar_texto(value)
        
        for dado in dados_banco:
            tipo_normalizado = normalizar_texto(dado[column])
            if comparar_strings(tipo_normalizado, termos_normalizados, precisao):
                resultados.append(dado)
                if get_one:
                    break
            

    return resultados

def get_item_compare(value, dados_banco, column, get_one = True, normatizar = False, reverse = False):
    resultados = []
    
    if value is not None:
        for dado in dados_banco:
            if compare_item_includes(value, dado[column], normatizar, reverse):
                resultados.append(dado)
                if get_one:
                    break
    
    return resultados


def compare_item_includes(value_1, value_2, normatizar = False, reverse = False):
    if value_1 is None or value_2 is None:
        return False
    if normatizar:
        value_1 = normalizar_texto(value_1)
        value_2 = normalizar_texto(value_2)
    if reverse:
        if value_1 in value_2:
            return True
    else:
        if value_2 in value_1:
            return True
    
    return False

def get_only_numbers(value):
    if (isinstance(value, float) and math.isnan(value)) or value is None:
        return ''
    numbers = re.findall(r'\d+', str(value))
    return ''.join(numbers)

def get_only_numbers_float(value):
    if (isinstance(value, float) and math.isnan(value)) or value is None:
        return ''
    if isinstance(value, (float, str)):
        numbers = re.findall(r'\d+\.?\d*', str(value))
        return ''.join(numbers)
    numbers = re.findall(r'\d+', str(value))
    return ''.join(numbers)