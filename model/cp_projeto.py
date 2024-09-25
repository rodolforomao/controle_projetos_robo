import pyodbc
import math
import model.db as db

import model.cp_tipo_projeto as cp_tipo_projeto
import model.tb_disciplinas_servicos as tb_disciplinas_servicos
import model.cp_vinculo_excel_documento as cp_vinculo_excel_documento
import model.supra as supra
import model.cp_documento as cp_documento
import model.cp_disciplina_contrato as cp_disciplina_contrato

from datetime import datetime

import config.config as config

TABLE_NAME = 'cp_projeto'
COLUMN_ID = 'id_projeto'

def get_columns():
    return (
        'id_tipo_projeto',
        'id_disciplina',
        'data',
        'id_documento',
        'id_cp_contrato',
        'id_usuario',
        'ultima_alteracao',
        'publicar',
        'data_publicar',
        'id_usuario_nao_publicar',
    )
    
def get_db_all_items():
    return db.get_select(TABLE_NAME)


def insertCpProjeto(row, lastRow):

    lastRow = None if lastRow is None else lastRow['FASE']
    #id_tipo_projeto = cp_tipo_projeto.get_id_tipo_projeto(row['FASE'], lastRow )
    id_tipo_projeto = cp_tipo_projeto.get_id_tipo_projeto(row)
    id_disciplinas_servicos = tb_disciplinas_servicos.get_id_tipo_disciplina(row)

    values = (
            id_tipo_projeto, # [id_tipo_projeto] ************ CONVERTER EM ID
            id_disciplinas_servicos, # ,[id_disciplina]  ********** CONVERTER EM ID
            row['data'],# ,[data] = data_encaminhamento
            row['id_documento'], # ,[id_documento]
            row['id_cp_contrato'], # ,[id_cp_contrato]
            supra.CONST_ID_USUARIO_SUPRA, # ,[id_usuario]
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # ,[ultima_alteracao]
            'S', # ,[publicar]
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # ,[data_publicar]
            None, # ,[id_usuario_nao_publicar]
    )
    
    return db.insert_query_generic(TABLE_NAME, get_columns() ,values, COLUMN_ID)


def updateCpProjeto(row, lastRow):
    lastRow = None if lastRow is None else lastRow['FASE']
    #id_tipo_projeto = cp_tipo_projeto.get_id_tipo_projeto(row['FASE'], lastRow )
    id_tipo_projeto = cp_tipo_projeto.get_id_tipo_projeto(row)
    id_disciplinas_servicos = tb_disciplinas_servicos.get_id_tipo_disciplina(row)
    id_projeto = row['id_projeto']
    values = (
            id_tipo_projeto,
            id_disciplinas_servicos,
            row['data'],
            row['id_documento'],
            row['id_cp_contrato'],
            supra.CONST_ID_USUARIO_SUPRA,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'S',
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            None,
    )
    
    return db.update_query_generic(TABLE_NAME, get_columns() , values, COLUMN_ID, id_projeto)
    

def checkExists(row, lastRow):
    #id_tipo_projeto = cp_tipo_projeto.get_id_tipo_projeto(row['FASE'], lastRow )
    id_tipo_projeto = cp_tipo_projeto.get_id_tipo_projeto(row)
    id_disciplinas_servicos = tb_disciplinas_servicos.get_id_tipo_disciplina(row)
    id_documento = row['id_documento']
    
    query = """
        SELECT * FROM """ + TABLE_NAME + """
            WHERE id_documento = """ + str(id_documento) + """
                and id_disciplina = """ + str(id_disciplinas_servicos) + """
                and id_tipo_projeto = """ + str(id_tipo_projeto) + """
    """
    
    return db.get_select_query(query)


def checkInsertOrUpdate(row, lastRow):
    id_item = 0
    exists, changed, id_item = checkExistsOrChanged(row, lastRow)
    insert_operation = True

    if exists:
        if changed:
            insert_operation = False
        else:
            return id_item
    
    row['data'] = cp_documento.get_data_encaminhamento(row)
    
    if insert_operation:
        id_disciplina_contrato = cp_disciplina_contrato.checkAndInsert(row)
        id_item = insertCpProjeto(row, lastRow)
    else:
        row[COLUMN_ID] = id_item
        id_item = updateCpProjeto(row, lastRow)
    
    if type(id_item) != str and type(id_item) != int and math.isnan(id_item):
        return False
    
    return id_item



def checkExistsOrChanged(row, lastRow):
    #result = checkExists(row, lastRow)
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
        cursor = conn.cursor()
        query = """
            SELECT * FROM [""" + TABLE_NAME + """]
            WHERE 
            id_tipo_projeto = """ + str(values['id_tipo_projeto']) +"""
            AND id_disciplina = """ + str(values['id_disciplina']) +"""
            """
            
        if values['data'] is None:
            query += """ 
                AND data is null 
                """
        else:
            query += """ 
                    AND data = '""" + str(values['data']) + """' 
                """
            
        query += """
            AND id_documento = """ + str(values['id_documento']) + """
            AND id_cp_contrato = """ + str(values['id_cp_contrato']) + """
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