import re
import math
import unicodedata
import pandas as pd
import logging

from fuzzywuzzy import fuzz

import model.db as db
import util.string_format as string_format


TABLE_NAME = 'cp_tipo_projeto'
COLUMN_ID = 'id_tipo_projeto'

NAME_COLUMN = 'tipo'

def get_db_all_items():
    return db.get_select(TABLE_NAME)



TIPO_PROJETO_IMPRESSAO_DEFINITIVA_FROM = 'Impressão Definitiva'
TIPO_PROJETO_IMPRESSAO_DEFINITIVA_TO = 'Proj. Básico/Executivo'

TIPO_PROJETO_ESTUDOS_PRELIMINARES_FROM = 'Estudos Preliminares'
TIPO_PROJETO_ESTUDOS_TO = 'Estudos'
TIPO_PROJETO_RELATORIO = 'Relatório'

TIPO_PROJETO_CONCEPCAO_FROM = 'Concepção'
TIPO_PROJETO_ANTEPROJETO_FROM = 'Anteprojeto'
TIPO_PROJETO_CONCEPCAO_ANTEPROJETO_TO = 'Concepção/Anteprojeto'

TIPO_PROJETO_PROJETO_BASICO_SIGLA_FROM = 'PB'
TIPO_PROJETO_PROJETO_BASICO_TO = 'Projeto Básico'

TIPO_PROJETO_PROJETO_EXECUTIVO_SIGLA_FROM = 'PE'
TIPO_PROJETO_PROJETO_EXECUTIVO_TO = 'Projeto Executivo'

TIPO_PROJETO_RELATORIO_PLANEJAMENTO = 'Relatório de Planejamento'

import util.recursive_verify as recursive_verify
import util.log as log
def get_id_tipo_projeto(row):
    
    value = recursive_verify.get_data_key(row,'FASE')
    contrato = recursive_verify.get_data_key(row,'contrato')
    titulo = 'Tipo projeto'
    
    if value is pd.NaT:
        value2 = recursive_verify.get_data_key(row,'DISCIPLINA')
        if value2 is pd.NaT:
            return False
        value = value2
    
    if type(value) == float and math.isnan(value):
        value2 = recursive_verify.get_data_key(row,'DISCIPLINA')
        if type(value2) == float and math.isnan(value2):
            return False
        value = value2
    
    if value.strip() == '-' or value.strip() == '':
        value = recursive_verify.get_data_key(row,'DISCIPLINA')
        #return False
    
    dados = get_tipo_projeto(value)
    if len(dados) > 0:
        for item in dados:
            log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + item[NAME_COLUMN], logging.INFO)
            return item[COLUMN_ID]
    
    if string_format.comparar_strings(TIPO_PROJETO_IMPRESSAO_DEFINITIVA_FROM, value,90):
        tipo_procurado = TIPO_PROJETO_IMPRESSAO_DEFINITIVA_TO
        dados = get_tipo_projeto(tipo_procurado)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
            
    if string_format.comparar_strings(TIPO_PROJETO_ESTUDOS_PRELIMINARES_FROM, value,90):
        tipo_procurado = TIPO_PROJETO_ESTUDOS_TO
        dados = get_tipo_projeto(tipo_procurado)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
            
    if string_format.comparar_strings(TIPO_PROJETO_RELATORIO_PLANEJAMENTO, value,90):
        tipo_procurado = TIPO_PROJETO_ESTUDOS_TO
        dados = get_tipo_projeto(tipo_procurado)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
    
    if string_format.comparar_strings(TIPO_PROJETO_CONCEPCAO_FROM, value,90) or string_format.comparar_strings(TIPO_PROJETO_ANTEPROJETO_FROM, value,90):
        tipo_procurado = TIPO_PROJETO_CONCEPCAO_ANTEPROJETO_TO
        dados = get_tipo_projeto(tipo_procurado)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
    
    if string_format.compare_item_includes(value, TIPO_PROJETO_PROJETO_BASICO_SIGLA_FROM, True):
        tipo_procurado = TIPO_PROJETO_PROJETO_BASICO_TO
        dados = get_tipo_projeto(tipo_procurado)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
            

    if string_format.compare_item_includes(value, TIPO_PROJETO_PROJETO_EXECUTIVO_SIGLA_FROM, True):
        tipo_procurado = TIPO_PROJETO_PROJETO_EXECUTIVO_TO
        dados = get_tipo_projeto(tipo_procurado)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
            
    if string_format.compare_item_includes(value, TIPO_PROJETO_RELATORIO, True):
        tipo_procurado = TIPO_PROJETO_ESTUDOS_TO
        dados = get_tipo_projeto(tipo_procurado)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
    
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

