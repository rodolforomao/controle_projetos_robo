import re
import math


import config.config as config

import model.db as db

import util.data_frame as data_frame
import util.string_format as string_format
import util.sei as sei
import util.datetime as datetime_class
from datetime import datetime

CONST_COLUMN_NUMERO_PROCESSO = 'Numero do Processo'
CONST_COLUMN_ORIGEM = 'Origem'
CONST_COLUMN_DESTINO = 'Destino'

CONST_COLUMN_TIPO_DOCUMENTO = 'RAP'
CONST_COLUMN_NAME_RAP = 'RAP'

CONST_ID_USUARIO_SUPRA = 3266

def migracao_dados(df, file):
    numero_contrato = get_contract(file)
    numero_processo_sei = extract_numero_processo(df)

    id_contrato = db.get_supra_contrato(numero_contrato)
    lista_origem_destino = db.get_supra_origem_destino()
    lista_tipo_documento = db.get_supra_tipo_documento()
    
    id_usuario_supra = CONST_ID_USUARIO_SUPRA

    GET_FIRST_VALID_VALUE = True
    id_origem = get_id_origem_destino(lista_origem_destino, data_frame.get_column(
        df, CONST_COLUMN_ORIGEM, GET_FIRST_VALID_VALUE)),  # origem (ajuste conforme necessário)
    
    if isinstance(id_origem, tuple):
        id_origem = id_origem[0]
        
    id_destino = get_id_origem_destino(lista_origem_destino, data_frame.get_column(
        df, CONST_COLUMN_DESTINO, GET_FIRST_VALID_VALUE)),  # destino (ajuste conforme necessário)
    
    if isinstance(id_destino, tuple):
        id_destino = id_destino[0]
        
    id_tipo_documento = get_id_tipo_documento(lista_tipo_documento, CONST_COLUMN_TIPO_DOCUMENTO)  # destino (ajuste conforme necessário)
    
    if isinstance(id_tipo_documento, tuple):
        id_tipo_documento = id_tipo_documento[0]

    insert_values = []
    count = 0
    for index, row in df.iterrows():
        id_documento = row['ID']
        fase = row['FASE']
        disciplina = row['DISCIPLINA']
        lote = row['LOTE']
        versao = row['VERSÃO']
        status = row['STATUS']
        unidade = row['UNIDADE']
        cronograma_aprov = row['CRONOGRAMA APROV.']
        data_entrega = row['DATA DA ENTREGA']
        protocolo = row['PROTOCOLO']
        rap = row['RAP']
        data_rap = row['DATA RAP']
        termo_aceite = row['TERMO DE ACEITE']
                
        numero_sei = get_numero_sei(termo_aceite, rap)
        try:
            data_encaminhamento = data_rap if data_rap else data_entrega
            if isinstance(data_encaminhamento, str):
                data_encaminhamento = datetime_class.clean_date_time(data_encaminhamento)
            if data_encaminhamento is not None:
                if isinstance(data_encaminhamento, datetime):
                    data_encaminhamento = data_encaminhamento.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    data_encaminhamento = None
        except ValueError as e:
            print(f"Invalid date: {e}")
            
            
        assunto = data_frame.get_column(df, CONST_COLUMN_NUMERO_PROCESSO, GET_FIRST_VALID_VALUE)
        observacao = get_observacao(row)
        ultima_alteracao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        documento_sei = sei.get_sei_document(data_frame.get_column(df, CONST_COLUMN_NAME_RAP, GET_FIRST_VALID_VALUE))
        publicar = 'S'
        data_publicar = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if check_exists(row):
            continue
        
        # Montando os valores para o INSERT
        insert_values.append(
            (
                id_contrato,
                numero_sei,
                data_encaminhamento,
                id_origem,
                id_destino,
                assunto,
                observacao,
                id_usuario_supra,
                ultima_alteracao,
                id_tipo_documento,
                numero_processo_sei,
                documento_sei,
                publicar,
                data_publicar,
                id_usuario_supra,
            )
        )

        # Se atingiu 100 valores ou está no final do loop, realiza o insert
        if len(insert_values) == 100 or count == len(df) - 1:
            db.insert_query(insert_values)
            
        count += 1
    print('')

def check_exists(row):
    print('')
    return True



def get_observacao(row):
    observacao = ""
    for column in row.index:
        observacao += f"{column}: {row[column]}\n"
    return observacao.strip()


def get_numero_sei(termo_aceite, rap):
    num_sei = get_sei_document(termo_aceite)
    if num_sei is None:
        num_sei = get_sei_document(rap)
    return num_sei

def get_sei_document(text):
    return sei.get_sei_document(text)
    


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
