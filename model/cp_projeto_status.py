import math
import pyodbc
from datetime import datetime

import model.db as db
import model.cp_status as cp_status
import model.cp_vinculo_excel_documento as cp_vinculo_excel_documento
import model.supra as supra

import util.string_format as string_format

import config.config as config

TABLE_NAME = 'cp_projeto_status'
COLUMN_ID = 'id_projeto_status'
NAME_COLUMN = 'nome'

def get_columns():
    return (
      'id_projeto',
      'id_status',
      'id_cp_contrato',
      'id_documento',
      'id_projeto_br',
      'id_usuario',
      'ultima_alteracao',
      'publicar',
      'data_publicar',
      'id_usuario_nao_publicar',
    )
    
    
def get_db_all_items():
    return db.get_select(TABLE_NAME)
  
  
def get_projeto_status(value):
  dados = get_status(value)
  if len(dados) > 0:
      for item in dados:
          return item[COLUMN_ID]
  return False

def get_status(value):
    return string_format.get_item(value, get_db_all_items(),NAME_COLUMN)


def insertCpProjetoStatus(row):
    id_status = get_id_status(row)
    values = (
            row['id_projeto'], # ,[id_projeto]
            id_status,# ,[id_status] -- nullable
            row['id_cp_contrato'], # ,[id_cp_contrato]
            row['id_documento'], # ,[id_documento]
            row['id_projeto_br'], # ,[id_projeto_br]
            supra.CONST_ID_USUARIO_SUPRA, # ,[id_usuario]
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # ,[ultima_alteracao]
            'S', # ,[publicar]
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # ,[data_publicar]
            None,# ,[id_usuario_nao_publicar]
    )
    
    # 'id_projeto',
    #   'id_status',
    #   'id_cp_contrato',
    #   'id_documento',
    #   'id_projeto_br',
    #   'publicar',
    #   'id_usuario',
    #   'ultima_alteracao',
    #   'data_publicar',
    #   'id_usuario_nao_publicar',
    return db.insert_query_generic(TABLE_NAME, get_columns() ,values, COLUMN_ID)
    
def updateCpProjetoStatus(row):
    id_status = get_id_status(row)
    id_projeto_status = row['id_projeto_status']
    
    values = (
            row['id_projeto'], # ,[id_projeto]
            id_status,# ,[id_status] -- nullable
            row['id_cp_contrato'], # ,[id_cp_contrato]
            row['id_documento'], # ,[id_documento]
            row['id_projeto_br'], # ,[id_projeto_br]
            supra.CONST_ID_USUARIO_SUPRA, # ,[id_usuario]
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # ,[ultima_alteracao]
            'S', # ,[publicar]
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # ,[data_publicar]
            None,# ,[id_usuario_nao_publicar]
    )
    
    return db.update_query_generic(TABLE_NAME, get_columns() ,values, COLUMN_ID, id_projeto_status)

def checkInsertOrUpdate(row):
    id_item = 0
    exists, changed, id_item = checkExistsOrChanged(row)
    insert_operation = True

    if exists:
        if changed:
            insert_operation = False
        else:
            return id_item
    
    if insert_operation:
        id_item = insertCpProjetoStatus(row)
    else:
        row[COLUMN_ID] = id_item
        id_item = updateCpProjetoStatus(row)
    
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
            
        result = checkChanged(row)
            
        if result:
            return True, False, id_item
        
        return True, True, id_item
    
    return False, False, 0

def checkChanged(values):
    try:
        conn = pyodbc.connect(
            db.get_connection_string(
                config.supra_db['server'],
                config.supra_db['db'],
                config.supra_db['user'],
                config.supra_db['pwd']
            )
        )
        
        id_documento = values['id_documento']
        id_projeto = values['id_projeto']
        id_projeto_br = values['id_projeto_br']
        id_status = get_id_status(values)
        
        
        
        cursor = conn.cursor()
        query = """
            SELECT * FROM """ + TABLE_NAME + """
            WHERE 
            [id_projeto] = '""" + str(id_projeto) + """'
            """
        if id_status is None:
            query +=   """
                        AND [id_status] is null
                        """
        else:
            query +=   """
                        AND [id_status] = '""" + str(id_status) + """'
                        """
        query +=   """
            and [id_cp_contrato] = '""" + str(values['id_cp_contrato']) + """'
            and [id_documento] = '""" + str(id_documento) + """'
            and [id_projeto_br] = '""" + str(id_projeto_br) + """'
        """
        cursor.execute(query)
        result = cursor.fetchall()
            
        return result
    except pyodbc.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        cursor.close()
        conn.close()
        
import util.recursive_verify as recursive_verify
def get_id_status(row):
    status = recursive_verify.get_data_key(row,'STATUS')
    if status is None:
        return None
    
    if isinstance(row['STATUS'], float) and math.isnan(row['STATUS']):
        id_status = None
    else:
        id_status = cp_status.get_status_converting_status(row['STATUS'])
        if len(id_status) > 0:
            for item in id_status:
                id_status = item['id_status']
        else:
            id_status = None
            
    return id_status