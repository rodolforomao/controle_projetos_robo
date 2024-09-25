import pyodbc
import math
from datetime import datetime
import pandas as pd

import util.data_frame as data_frame
import util.datetime as datetime_class
import util.sei as sei
import util.query as queryUtil
import util.recursive_verify as recursive_verify

import model.db as db
import model.cp_vinculo_excel_documento as cp_vinculo_excel_documento
import model.supra as supra

import config.config as config

TABLE_NAME = 'cp_documento'
COLUMN_ID = 'id_documento'

CONST_COLUMN_NAME_RAP = 'RAP'

def insert_query(insert_values):
    try:
        conn = pyodbc.connect(db.get_connection_string(
            config.supra_db['server'],
            config.supra_db['db'],
            config.supra_db['user'],
            config.supra_db['pwd']
        ))
        cursor = conn.cursor()

        # Inserindo os valores
        insert_query = """
            INSERT INTO [SUPRA].[dbo].["""+ TABLE_NAME +"""] 
            (
                
                [id_cp_contrato],
                [numero_sei],
                [data_encaminhamento],
                [id_origem],
                [id_destino],
                [assunto],
                [observacao],
                [id_usuario],
                [ultima_alteracao],
                [id_tipo],
                [processo_sei],
                [documento_sei],
                [publicar],
                [data_publicar],
                [id_usuario_nao_publicar]
            ) 
            OUTPUT INSERTED.["""+ COLUMN_ID +"""] 
            VALUES (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ? 
                )
        """
        
        queryUtil.get_raw_query(insert_query, insert_values)
        cursor.execute(insert_query, insert_values)
        inserted_id = cursor.fetchone()[0] 
        conn.commit()
        return inserted_id 
    except pyodbc.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
            cursor.close()
            conn.close()
            
def update_query(values, id_documento, return_id_documento = False):
    try:
        conn = pyodbc.connect(db.get_connection_string(
            config.supra_db['server'],
            config.supra_db['db'],
            config.supra_db['user'],
            config.supra_db['pwd']
        ))
        cursor = conn.cursor()

          # Preparing the query
        query = """
            UPDATE [SUPRA].[dbo].["""+ TABLE_NAME +"""] 
            SET 
                [id_cp_contrato] = ?,
                [numero_sei] = ?,
                [data_encaminhamento] = ?,
                [id_origem] = ?,
                [id_destino] = ?,
                [assunto] = ?,
                [observacao] = ?,
                [id_usuario] = ?,
                [ultima_alteracao] = ?,
                [id_tipo] = ?,
                [processo_sei] = ?,
                [documento_sei] = ?,
                [publicar] = ?,
                [data_publicar] = ?,
                [id_usuario_nao_publicar] = ?
            WHERE ["""+ COLUMN_ID +"""] = ?
        """

        cursor.execute(query, values + (id_documento,))
        
        conn.commit()
        if cursor.rowcount == -1:
            return id_documento
        else:
            if return_id_documento:
                return id_documento
            return cursor.rowcount
    except pyodbc.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    finally:
            cursor.close()
            conn.close()
            
import util.query as queryUtil
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
            id_cp_contrato = '""" + str(values["id_cp_contrato"]).replace("'", "''") +"""'
            """
        
        query += queryUtil.checkIsNull('numero_sei', values)
        query += queryUtil.checkIsNull("data", values, 'data_encaminhamento')
        
        query += queryUtil.checkIsNull("origem", values, 'id_origem')
        query += queryUtil.checkIsNull("destino", values, 'id_destino')
        query += queryUtil.checkIsNull("assunto", values)
        query += queryUtil.checkIsNull("observacao", values)
        query += queryUtil.checkIsNull("id_tipo_documento", values,"id_tipo")
        query += queryUtil.checkIsNull("processo_sei", values)
        query += queryUtil.checkIsNull("documento_sei", values)
        
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
   
def checkExistsOrChanged(row):
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
    

        

def checkInsertOrUpdate(row, df):
   
    protocolo = row['PROTOCOLO']
    rap = row['RAP']
    termo_aceite = row['TERMO DE ACEITE']
            
    numero_sei = sei.get_numero_sei(termo_aceite, rap)
    data_encaminhamento = get_data_encaminhamento(row)
        
    #assunto = data_frame.get_column(df, CONST_COLUMN_NUMERO_PROCESSO, GET_FIRST_VALID_VALUE)
    assunto = protocolo
    if type(assunto) != str and math.isnan(assunto):
        assunto = None
    observacao = get_observacao(row)
    ultima_alteracao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    GET_FIRST_VALID_VALUE = True
    documento_sei = sei.get_sei_document(data_frame.get_column(df, CONST_COLUMN_NAME_RAP, GET_FIRST_VALID_VALUE))
    data_publicar = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    row['observacao'] = observacao
    row['numero_sei'] = numero_sei
    row['documento_sei'] = documento_sei
    row['assunto'] = assunto
    
    exists, changed, id_documento = checkExistsOrChanged(row)
    
    insert_operation = True
    # Existe e não teve alteração
    if exists:
        if changed:
            insert_operation = False
        else:
            return id_documento
    
    # Montando os valores para o INSERT
    list_values = (
            row['id_cp_contrato'],
            numero_sei,
            data_encaminhamento,
            row['origem'],
            row['destino'],
            assunto,
            observacao,
            supra.CONST_ID_USUARIO_SUPRA,
            ultima_alteracao,
            row['id_tipo_documento'],
            row['processo_sei'],
            documento_sei,
            'S',
            data_publicar,
            None,
    )

    # Se atingiu 100 valores ou está no final do loop, realiza o insert
    #if len(insert_values) == 100 or count == len(df) - 1:
    if insert_operation:
        id_documento = insert_query(list_values)
    else:
        return_id_documento = True
        id_documento = update_query(list_values, id_documento, return_id_documento)
            
    if type(id_documento) != str and type(id_documento) != int and math.isnan(assunto):
        return False
    return id_documento


def get_observacao(row):
    observacao = ""
    for column in row.index:
        observacao += f"{column}: {row[column]}\n"
    return observacao.strip()



def get_data_encaminhamento(row):
    #data_entrega = row['DATA DA ENTREGA']
    data_entrega = recursive_verify.get_data_key(row,'DATA DA ENTREGA')
    if data_entrega is None:
        useFuzzToCompare = True
        data_entrega = recursive_verify.get_data_key(row,'DATA DA ENTREGA', useFuzzToCompare)
    #data_rap = row['DATA RAP']
    data_rap = recursive_verify.get_data_key(row,'DATA RAP')
    if data_rap is None:
        useFuzzToCompare = True
        data_rap = recursive_verify.get_data_key(row,'DATA RAP', useFuzzToCompare, 85)
    if data_entrega == '-':
        data_entrega = None
    if data_rap == '-':
        data_rap = None
    data_encaminhamento = None
    try:
        scapNextStep = False
        data_encaminhamento = data_rap if data_rap else data_entrega
        if isinstance(data_encaminhamento, str):
            data_encaminhamento = datetime_class.clean_date_time(data_encaminhamento)
        if data_encaminhamento is not None :
            if isinstance(data_encaminhamento, datetime) and data_encaminhamento is not pd.NaT:
                data_encaminhamento = data_encaminhamento.strftime('%Y-%m-%d %H:%M:%S')
            if data_encaminhamento is None:
                data_encaminhamento = None
            if data_encaminhamento is pd.NaT:
                data_encaminhamento = None
                scapNextStep = True
                
        if scapNextStep == False:
            if type(data_encaminhamento) != str and  math.isnan(data_encaminhamento):
                data_encaminhamento = None
            
    except ValueError as e:
        print(f"Invalid date: {e}")
        
    return data_encaminhamento