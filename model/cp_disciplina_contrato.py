
import pyodbc

from datetime import datetime

import model.db as db

import util.query as queryUtil

import config.config as config

TABLE_NAME = 'cp_contrato_disciplina'
COLUMN_ID = 'id_contrato_disciplina'

def get_columns():
    return (
      'id_cp_contrato'
      ,'id_servico'
      ,'id_usuario'
      ,'ultima_alteracao'
      ,'km_inicial'
      ,'km_final'
      ,'publicar'
      ,'data_publicar'
      ,'id_usuario_nao_publicar'
    )


def checkAndInsert(row):
      result = checkChanged(row)
      
      if(type(result) != int and (len(result) == 0 or result is None)):
        result = insert(row)
        
      return result

def insert(row):

    values = (
            row['id_cp_contrato'],
            row['id_disciplina'],
            3266,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            None,
            None,
            'S', 
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            None,
    )
    
    return db.insert_query_generic(TABLE_NAME, get_columns() ,values, COLUMN_ID)
  

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
        COLUMN_ID_SERVICO = 'id_disciplina'
        cursor = conn.cursor()
        query = """
            SELECT * FROM """ + TABLE_NAME + """ WHERE id_cp_contrato = '""" + str(values["id_cp_contrato"]).replace("'", "''") +"""' and id_servico = '""" + str(values[COLUMN_ID_SERVICO]) +"""'
            """
                
        cursor.execute(query)
        result = cursor.fetchall()
        
        if len(result):
              item = result[0]
              if len(item):
                    item_id = item[0]
                    return item_id 
            
        return result
    except pyodbc.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        cursor.close()
        conn.close()