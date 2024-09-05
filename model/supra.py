import re
import math

from datetime import datetime

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

import model.pandas as pandas

import util.data_frame as data_frame
import util.string_format as string_format
import util.sei as sei
import util.datetime as datetime_class

CONST_COLUMN_NUMERO_PROCESSO = 'Numero do Processo'
CONST_COLUMN_ORIGEM = 'Origem'
CONST_COLUMN_DESTINO = 'Destino'

CONST_COLUMN_TIPO_DOCUMENTO = 'RAP'
CONST_COLUMN_NAME_RAP = 'RAP'

CONST_ID_USUARIO_SUPRA = 3266


    
def migracao_dados(df, file):
    
    
    numero_processo_sei, id_contrato, id_origem, id_destino, id_tipo_documento = get_initials_parameters(df, file)
    ################################
    # EXTRAÇÃO DE DADOS
    ################################
   
    insert_values = []
    count = 0
    lastRow = None
            
    for index, row in df.iterrows():
        try:
            # General parameters
            row['id_contrato_obra'] = id_contrato
            row['processo_sei'] = numero_processo_sei
            row['origem'] = id_origem
            row['destino'] = id_destino
            row['id_tipo_documento'] = id_tipo_documento
            id_disciplinas_servicos = tb_disciplinas_servicos.get_id_tipo_disciplina(row['DISCIPLINA'])
            row['id_disciplina'] = id_disciplinas_servicos
            row['id_tipo_projeto'] = cp_tipo_projeto.get_id_tipo_projeto(row['FASE'], lastRow )
            data_encaminhamento = cp_documento.get_data_encaminhamento(row)
            row['data'] = data_encaminhamento
            
            id_documento = cp_documento.checkInsertOrUpdate(row, df)
            row['id_documento'] = id_documento
            
            if id_documento > 0:
            #     #2 - INSERT CP_PROJETO
                id_projeto = cp_projeto.checkInsertOrUpdate( row, lastRow)
                row['id_projeto'] = id_projeto
                    
            #3 - INSERT CP_PROJETO_BR
            if id_documento > 0 and id_projeto > 0:
                id_projeto_br = cp_projeto_br.checkInsertOrUpdate(row)
                row['id_projeto_br'] = id_projeto_br
            
            if id_documento > 0 and id_projeto > 0 and id_projeto_br > 0:
            #4 - INSERT CP_PROJETO_STATUS
                id_projeto_status = cp_projeto_status.checkInsertOrUpdate(row)
                row['id_projeto_status'] = id_projeto_status
                
            if id_documento > 0 and id_projeto > 0 and id_projeto_br > 0 and id_projeto_status > 0:
                cp_vinculo_excel_documento.checkInsert(row)
                
        except Exception as e:
            print(f"Foreach: {e}")
        lastRow = row
        print(count)
        count += 1
    print('finalizando')

    
def get_initials_parameters(df, file):
    ################################
    # EXTRAÇÃO DE DADOS
    ################################
    
    # número processo sei
    numero_processo_sei = extract_numero_processo(df)

    # id contrato obra
    id_contrato = db.get_supra_contrato(get_contract(file))
    

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
        
    return numero_processo_sei, id_contrato, id_origem, id_destino, id_tipo_documento


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
