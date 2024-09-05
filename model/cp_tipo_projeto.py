import re
import unicodedata
from fuzzywuzzy import fuzz

import model.db as db

TABLE_NAME = 'cp_tipo_projeto'
COLUMN_ID_CAME = 'id_tipo_projeto'

NAME_COLUMN = 'tipo'

def get_db_all_items():
    return db.get_select(TABLE_NAME)

import util.string_format as string_format

TIPO_PROJETO_IMPRESSAO_DEFINITIVA = 'Impressão Definitiva'
TIPO_PROJETO_IMPRESSAO_DEFINITIVA_CONVERT = 'Proj. Básico/Executivo'

TIPO_PROJETO_ESTUDOS_PRELIMINARES_FULL = 'Estudos Preliminares'
TIPO_PROJETO_ESTUDOS_PRELIMINARES = 'Estudos'

def get_id_tipo_projeto(value, last_value):
    dados = get_tipo_projeto(value)
    if len(dados) > 0:
        for item in dados:
            return item[COLUMN_ID_CAME]
    
    if string_format.comparar_strings(TIPO_PROJETO_IMPRESSAO_DEFINITIVA, value,90):
        dados = get_tipo_projeto(TIPO_PROJETO_IMPRESSAO_DEFINITIVA_CONVERT)
        if len(dados) > 0:
            for item in dados:
                return item[COLUMN_ID_CAME]
            
    if string_format.comparar_strings(TIPO_PROJETO_ESTUDOS_PRELIMINARES_FULL, value,90):
        dados = get_tipo_projeto(TIPO_PROJETO_ESTUDOS_PRELIMINARES)
        if len(dados) > 0:
            for item in dados:
                return item[COLUMN_ID_CAME]
        
    return False

def get_tipo_projeto(value):
    return get_item(value, get_db_all_items(),NAME_COLUMN)

# TIPO_IMPRESSAO_DEFINITIVA = "Impressão Definitiva"
# TIPO_IMPRESSAO_DEFINITIVA_WILLBE_PROJ_BASICO_EXECUTIVO = "Proj. Basico/Executivo"

import model.tb_disciplinas_servicos as tb_disciplinas_servicos

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
            # else:
            #     if string_format.comparar_strings(TIPO_IMPRESSAO_DEFINITIVA, value,95, True):
            #         dados = tb_disciplinas_servicos.get_tipo_disciplina(TIPO_IMPRESSAO_DEFINITIVA)
            #     if len(dados) > 0:
            #         for item in dados:
            #             return item[tb_disciplinas_servicos.COLUMN_ID]

    return resultados

def normalizar_texto(texto):
    if texto is not None and len(texto) > 0:
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
        texto = re.sub(r'[^a-zA-Z0-9]', '', texto).lower()
        return texto
    return ''

def comparar_strings(string1, string2, limiar=80, normalizar = False):
    if normalizar:
        string1 = normalizar_texto(string1)
        string2 = normalizar_texto(string2)
    similaridade = fuzz.ratio(string1, string2)
    return similaridade >= limiar

