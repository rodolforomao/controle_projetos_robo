import re
import math

from datetime import datetime

import logging

import config.config as config

import model.db as db

import model.cp_projeto as cp_projeto
import model.cp_tipo_projeto as cp_tipo_projeto
import model.tb_disciplinas_servicos as tb_disciplinas_servicos
import model.tb_contrato_obra as tb_contrato_obra
import model.cp_projeto_br as cp_projeto_br
import model.cp_projeto_status as cp_projeto_status
import model.cp_status as cp_status
import model.cp_origem_destino as cp_origem_destino
import model.cp_tipo as cp_tipo
import model.cp_vinculo_excel_documento as cp_vinculo_excel_documento
import model.cp_documento as cp_documento
import model.cp_contrato as cp_contrato

import model.pandas as pandas

import util.data_frame as data_frame
import util.string_format as string_format
import util.sei as sei
import util.datetime as datetime_class
import util.log as log

CONST_COLUMN_NUMERO_PROCESSO = 'Numero do Processo'
CONST_COLUMN_ORIGEM = 'Origem'
CONST_COLUMN_DESTINO = 'Destino'

CONST_COLUMN_TIPO_DOCUMENTO = 'RAP'
CONST_COLUMN_NAME_RAP = 'RAP'

CONST_ID_USUARIO_SUPRA = 3266

PRINT_LOGS = True
PRINT_LINES = False
PRINT_EMPTY_LINES = False
PRINT_LINES_DISCIPLINAS_NAO_ENCONTRADAS = False
PRINT_LINES_TIPO_PROJETO_NAO_ENCONTRADOS = True
PRINT_REPORT = True
    
import model.cp_contrato as cp_contrato
def migracao_dados(df, file):
    numero_processo_sei, id_cp_contrato, id_origem, id_destino, id_tipo_documento = get_initials_parameters(df, file)
    ################################
    # EXTRAÇÃO DE DADOS
    ################################
    contrato = get_contract(file)
    print('Número contrato:' + contrato)
    log.track(contrato, 'Iniciando migração', logging.INFO)
 
    contador = {
        'linhas vazias': 0,
        'sem ID': 0,
        'disciplinas não encontradas': 0,
        'tipo projeto não encontrado': 0
    }
   
    insert_values = []
    count = 0
    lastRow = None
            
    for index, row in df.iterrows():
        try:
            # General parameters
            #row['id_contrato_obra'] = id_contrato_obra
            #if(data_frame.is_row_empty(row,7)):
            if(data_frame.is_row_empty(row,2)):
                if PRINT_EMPTY_LINES:
                    print(f"{contrato} : Linha {index + 1} - LINHA VAZIA ('DISCIPLINA')| Index: {list(row.index)} | Values: {list(row.values)}")
                contador['linhas vazias'] += 1
                continue
            
            row['contrato'] = contrato
            row[cp_contrato.COLUMN_ID] = id_cp_contrato
            row['br'] = tb_contrato_obra.get_br_from_contrato(row[cp_contrato.COLUMN_ID])
            row['processo_sei'] = numero_processo_sei
            row['origem'] = id_origem
            row['destino'] = id_destino
            row['id_tipo_documento'] = id_tipo_documento
            id_disciplinas_servicos = tb_disciplinas_servicos.get_id_tipo_disciplina(row)
            if id_disciplinas_servicos == False:
                error_message = f"{contrato} : Linha {index + 1} - disciplina não encontrada  ('DISCIPLINA')| Index: {list(row.index)} | Values: {list(row.values)}"
                if PRINT_LINES:
                    print(count)
                if PRINT_LINES_DISCIPLINAS_NAO_ENCONTRADAS:
                    print(error_message)
                count += 1
                contador['disciplinas não encontradas'] += 1
                log.track(contrato, error_message)
                continue
            row['id_disciplina'] = id_disciplinas_servicos
            row['id_tipo_projeto'] = cp_tipo_projeto.get_id_tipo_projeto(row)
            if row['id_tipo_projeto'] == False:
                error_message = f"{contrato} : Linha {index + 1} - tipo de projeto não encontrado ('FASE') | Index: {list(row.index)} | Values: {list(row.values)}"
                if PRINT_LINES:
                    print(count)
                if PRINT_LINES_TIPO_PROJETO_NAO_ENCONTRADOS:
                    print(error_message)
                count += 1
                contador['tipo projeto não encontrado'] += 1
                log.track(contrato, error_message)
                continue
            if row.get('ID') == "-" or row.get('ID') == "" or (type(row.get('ID')) == str and row.get('ID').strip() == ""):
                error_message = f"{contrato} : Linha {index + 1} - ID VAZIO ('DISCIPLINA')| Index: {list(row.index)} | Values: {list(row.values)}"
                if PRINT_EMPTY_LINES:
                    print(error_message)
                contador['sem ID'] += 1
                log.track(contrato, error_message)
                continue
            data_encaminhamento = cp_documento.get_data_encaminhamento(row)
            row['data'] = data_encaminhamento
            
            try:
                id_documento = cp_documento.checkInsertOrUpdate(row, df)
                row['id_documento'] = id_documento
            except Exception as e:
                log.track(contrato, 'Erro ao inserir: cp_documento', logging.ERROR)
            
            if id_documento > 0:
            #     #2 - INSERT CP_PROJETO
                try:
                    id_projeto = cp_projeto.checkInsertOrUpdate( row, lastRow)
                    row['id_projeto'] = id_projeto
                except Exception as e:
                    log.track(contrato, 'Erro ao inserir: cp_projeto e cp_disciplina_contrato')
                    
            #3 - INSERT CP_PROJETO_BR
            if id_documento > 0 and id_projeto > 0:
                try:
                    id_projeto_br = cp_projeto_br.checkInsertOrUpdate(row)
                    row['id_projeto_br'] = id_projeto_br
                except Exception as e:
                    log.track(contrato, 'Erro ao inserir: cp_projeto_br')
            
            if id_documento > 0 and id_projeto > 0 and id_projeto_br > 0:
            #4 - INSERT CP_PROJETO_STATUS
                try:
                    id_projeto_status = cp_projeto_status.checkInsertOrUpdate(row)
                    row['id_projeto_status'] = id_projeto_status
                except Exception as e:
                    log.track(contrato, 'Erro ao inserir: cp_projeto_status')
                
            if id_documento > 0 and id_projeto > 0 and id_projeto_br > 0 and id_projeto_status > 0:
                try:
                    cp_vinculo_excel_documento.checkInsert(row)
                except Exception as e:
                    log.track(contrato, 'Erro ao inserir: cp_vinculo_excel_documento')
                
            log.track(contrato, 'Linha: ' + str(index + 1) + ' - inserido com sucesso.', logging.INFO)
            
        except Exception as e:
            print(f'Main foreach {e}')
            
        if PRINT_LINES:
            print(count)
        count += 1
        lastRow = row
    if PRINT_REPORT:
        if contador['linhas vazias'] > 0:
            error_message = f"Linhas vazias: {contador['linhas vazias']}"
            log.track(contrato, error_message)
            print(error_message)
        if contador['disciplinas não encontradas'] > 0:
            error_message = f"Disciplinas não encontradas: {contador['disciplinas não encontradas']}"
            log.track(contrato, error_message)
            print(error_message)
        if contador['tipo projeto não encontrado']:
            error_message = f"Tipo projeto não encontrado: {contador['tipo projeto não encontrado']}"
            log.track(contrato, error_message)
            print(error_message)
        if contador['sem ID']:
            error_message = f"Linha sem identificador: {contador['sem ID']}"
            log.track(contrato, error_message)
            print(error_message)
    
    print('finalizando')
    log.track(contrato,'Migração finalizada', logging.INFO)


def get_initials_parameters(df, file):
    ################################
    # EXTRAÇÃO DE DADOS
    ################################
    
    # número processo sei
    numero_processo_sei = extract_numero_processo(df)

    # id contrato obra
    #id_cp_contrato, id_contrato_obra = db.get_supra_contrato(get_contract(file))
    id_cp_contrato = cp_contrato.get_supra_contrato(get_contract(file))
    

    GET_FIRST_VALID_VALUE = True
    id_origem = get_id_origem_destino(cp_origem_destino.get_db_all_items(), data_frame.get_column(
        df, CONST_COLUMN_ORIGEM, GET_FIRST_VALID_VALUE)),  # origem (ajuste conforme necessário)
    
    if isinstance(id_origem, tuple):
        id_origem = id_origem[0]
        
    id_destino = get_id_origem_destino(cp_origem_destino.get_db_all_items(), data_frame.get_column(
        df, CONST_COLUMN_DESTINO, GET_FIRST_VALID_VALUE)),  # destino (ajuste conforme necessário)
    
    if isinstance(id_destino, tuple):
        id_destino = id_destino[0]
        
    id_tipo_documento = get_id_tipo_documento(cp_tipo.get_db_all_items(), CONST_COLUMN_TIPO_DOCUMENTO)  # destino (ajuste conforme necessário)
    
    if isinstance(id_tipo_documento, tuple):
        id_tipo_documento = id_tipo_documento[0]
        
    #return numero_processo_sei, id_cp_contrato, id_contrato_obra, id_origem, id_destino, id_tipo_documento
    return numero_processo_sei, id_cp_contrato, id_origem, id_destino, id_tipo_documento


def get_contract(text):
    pattern = r'\b(\d{2}) ?(\d{5})[./-]?(\d{2,4})\b'
    matches = re.findall(pattern, text)
    for match in matches:
        first_two = match[0]
        middle_five = match[1]
        year = match[2]

        # Garantir que o ano tenha 4 dígitos
        if len(year) == 2:
            year = "20" + year  # Supondo que os anos sejam dos 2000s

        # Formatar para '00 00000/0000'
        formatted_number = f"{first_two} {middle_five}/{year}"
        return formatted_number
    return None


def extract_numero_processo(df):
    numero_processo = data_frame.get_column(
        df, CONST_COLUMN_NUMERO_PROCESSO, True)
    if numero_processo is not None:
        return get_numero_processo(numero_processo)
    return None


def get_numero_processo(text):
    pattern = r'\b(\d{5})[.\s-]?(\d{6})[./\s-]?(\d{4})[./\s-]?(\d{2})\b'

    matches = re.findall(pattern, text)
    for match in matches:
        part1 = match[0]
        part2 = match[1]
        year = match[2]
        suffix = match[3]

        # Formatar para '00000.000000/0000-00'
        formatted_number = f"{part1}.{part2}/{year}-{suffix}"
        return formatted_number

    return None








def get_id_origem_destino(lista, nome):
    return get_value_and_compare(lista, nome,'nome','id_origem_destino')

CONST_COLUMN_TIPO = 'tipo'
CONST_COLUMN_ID_TIPO = 'id_tipo'
def get_id_tipo_documento(lista, nome):
    GET_EXACT_TEXT = False
    return get_value_and_compare(lista, nome,CONST_COLUMN_TIPO,CONST_COLUMN_ID_TIPO, GET_EXACT_TEXT)

def get_value_and_compare(lista, nome, column_1, column_2, exact=True):
    # Normaliza o nome de origem para a comparação
    nome_origem_normalizado = string_format.normalize_text(nome)

    for item in lista:
        # Normaliza o nome no item para a comparação
        nome_item_normalizado = string_format.normalize_text(item[column_1])

        if exact:
            if nome_item_normalizado == nome_origem_normalizado:
                return item[column_2]
        else:
            if nome_item_normalizado in nome_origem_normalizado or nome_origem_normalizado in nome_item_normalizado:
                return item[column_2]
    return None  # Retorna None se o nome não for encontrado
