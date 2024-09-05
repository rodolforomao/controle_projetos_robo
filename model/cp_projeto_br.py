import math
import pyodbc

from datetime import datetime

import model.tb_contrato_obra as tb_contrato_obra
import model.cp_tipo_projeto as cp_tipo_projeto
import model.tb_disciplinas_servicos as tb_disciplinas_servicos
import model.cp_vinculo_excel_documento as cp_vinculo_excel_documento
import model.supra as supra

import model.db as db

import util.string_format as string_format

import config.config as config

TABLE_NAME = 'cp_projeto_br'
COLUMN_ID = 'id_projeto_br'

def get_columns():
    return (
      'id_projeto',
      'br',
      'km_inicial',
      'km_final',
      'id_contrato_obra',
      'id_usuario',
      'ultima_alteracao',
      'id_documento',
      'publicar',
      'data_publicar',
      'id_usuario_nao_publicar',
    )


def insertCpProjetoBr(row):
    br = tb_contrato_obra.get_br_from_contrato(get_data.get_data_key(row,'id_contrato_obra'))
    km_inicial = string_format.get_only_numbers_float(get_data.get_data_key(row,'km_inicial'))
    km_final = string_format.get_only_numbers_float(get_data.get_data_key(row,'km_final'))

    values = (
            row['id_projeto'], # ,[id_projeto]
            br, # ,[br]
            km_inicial, # ,[km_inicial]
            km_final, # ,[km_final]
            row['id_contrato_obra'], # ,[id_contrato_obra]
            supra.CONST_ID_USUARIO_SUPRA, # ,[id_usuario]
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # ,[ultima_alteracao]
            row['id_documento'],# ,[id_documento]
            'S', # ,[publicar]
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # ,[data_publicar]
            None,# ,[id_usuario_nao_publicar]
    )
    
    return db.insert_query_generic(TABLE_NAME, get_columns() ,values, COLUMN_ID)
  
def updateCpProjetoBr(row):
    br = tb_contrato_obra.get_br_from_contrato(row['id_contrato_obra'])
    km_inicial = string_format.get_only_numbers_float(get_data.get_data_key(row,'km_inicial'))
    km_final = string_format.get_only_numbers_float(get_data.get_data_key(row,'km_final'))
    
    id_projeto_br = row['id_projeto_br']
    
    values = (
            row['id_projeto'], # ,[id_projeto]
            br, # ,[br]
            km_inicial, # ,[km_inicial]
            km_final, # ,[km_final]
            row['id_contrato_obra'], # ,[id_contrato_obra]
            supra.CONST_ID_USUARIO_SUPRA, # ,[id_usuario]
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # ,[ultima_alteracao]
            row['id_documento'],# ,[id_documento]
            'S', # ,[publicar]
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # ,[data_publicar]
            None,# ,[id_usuario_nao_publicar]
    )
    
    return db.update_query_generic(TABLE_NAME, get_columns() ,values, COLUMN_ID, id_projeto_br)
    
import model.cp_documento as cp_documento
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
        id_item = insertCpProjetoBr(row)
    else:
        row[COLUMN_ID] = id_item
        id_item = updateCpProjetoBr(row)
    
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
  
  
import util.recursive_verify as get_data
def checkExists(row):
  id_documento = row['id_documento']
  id_projeto = row['id_projeto']
  km_inicial = string_format.get_only_numbers_float(get_data.get_data_key(row,'km_inicial'))
  km_final = string_format.get_only_numbers_float(get_data.get_data_key(row,'km_final'))
  br = tb_contrato_obra.get_br_from_contrato(row['br'])
  
  query = """
      SELECT * FROM """ + TABLE_NAME + """
          WHERE id_documento = '""" + str(id_documento) + """'
              and km_inicial = '""" + str(km_inicial) + """'
              and km_final = '""" + str(km_final) + """'
              and id_projeto = '""" + str(id_projeto) + """'
              and br = '""" + str(br) + """'
  """
  
  return db.get_select_query(query)

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
        km_inicial = string_format.get_only_numbers_float(get_data.get_data_key(values,'km_inicial'))
        km_final = string_format.get_only_numbers_float(get_data.get_data_key(values,'km_final'))
        br = tb_contrato_obra.get_br_from_contrato(get_data.get_data_key(values,'id_contrato_obra'))
        
        cursor = conn.cursor()
        query = """
            SELECT * FROM """ + TABLE_NAME + """
          WHERE id_documento = '""" + str(id_documento) + """'
              and km_inicial = '""" + str(km_inicial) + """'
              and km_final = '""" + str(km_final) + """'
              and id_projeto = '""" + str(id_projeto) + """'
              and br = '""" + str(br) + """'
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