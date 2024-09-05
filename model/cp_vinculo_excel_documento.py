import math

from datetime import datetime

import model.db as db
import model.cp_status as cp_status
import model.cp_vinculo_excel_documento as cp_vinculo_excel_documento
import model.supra as supra

import util.string_format as string_format

TABLE_NAME = 'cp_vinculo_excel_documento'
COLUMN_ID = 'id_vinculo_excel_documento'
NAME_COLUMN = 'identificador'

def get_columns():
    return (
        'id_documento',
        'id_projeto',
        'id_projeto_br',
        'id_projeto_status',
        'id_contrato_obra',
        'id_origem',
        'id_destino',
        'identificador',
        'id_usuario',
        'ultima_alteracao',
        'publicar',
        'data_publicar',
        'id_usuario_nao_publicar'
    )
    
  
def insertCpVinculoExcelDocumento(row):
    id_line = string_format.get_only_numbers(row['ID'])
    values = (
            row['id_documento'],# ,[id_documento]
            row['id_projeto'],# [id_projeto]
            row['id_projeto_br'],#,[id_projeto_br]
            row['id_projeto_status'],#,[id_projeto_status]
            row['id_contrato_obra'], # ,[id_contrato_obra]
            row['origem'],#,[id_origem_destino]
            row['destino'],#,[id_origem_destino]
            id_line,
            supra.CONST_ID_USUARIO_SUPRA, # ,[id_usuario]
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # ,[ultima_alteracao]
            'S', # ,[publicar]
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # ,[data_publicar]
            None,# ,[id_usuario_nao_publicar]
    )
    
    return db.insert_query_generic(TABLE_NAME, get_columns() ,values, COLUMN_ID)
  
  
def verificarCpVinculoExcelDocumento(row):
  identificador = string_format.get_only_numbers(row['ID'])
  
  query = '''
    SELECT * FROM '''  + TABLE_NAME + ''' WHERE id_contrato_obra = ''' + str(row['id_contrato_obra']) + ''' AND identificador = ''' + str(identificador) + '''
  '''
  
  return db.get_select_query(query)
  
def get_id_origem_destino(lista, nome):
    return get_value_and_compare(lista, nome,'nome','id_origem_destino')  
  
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

def checkInsert(row):
    id_item = 0
    exists, changed, id_item = checkExistsOrChanged(row)
    insert_operation = True

    if exists:
        if changed:
            insert_operation = False
        else:
            return id_item
    
    if insert_operation:
        id_item = insertCpVinculoExcelDocumento(row)
    
    
    if type(id_item) != str and type(id_item) != int and math.isnan(id_item):
        return False
    
    return id_item
  

def checkExistsOrChanged(row,):
    #result = checkExists(row)
    result = cp_vinculo_excel_documento.verificarCpVinculoExcelDocumento(row)
    if result:
        id_item = 0
        for item in result:
            id_item = item[COLUMN_ID]
            
        return True, False, id_item
    
    return False, False, 0
  
  
  