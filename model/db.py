import pyodbc

import model.db as db
import model.cp_contrato as cp_contrato
import util.query as queryUtil

import config.config as config

def get_connection_string(server = 'localhost', database = 'SUPRA', username = 'teste', password = 'Ab1234567'):
    return f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'


def get_select_query(query):
    try:
        conn = pyodbc.connect(db.get_connection_string(
            config.supra_db['server'],
            config.supra_db['db'],
            config.supra_db['user'],
            config.supra_db['pwd']
        ))
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        result_list = [
            dict(zip([column[0] for column in cursor.description], row)) for row in results]
        return result_list

    except pyodbc.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

    finally:
        cursor.close()
        conn.close()

    return None

def get_select(table):
    try:
        conn = pyodbc.connect(db.get_connection_string(
            config.supra_db['server'],
            config.supra_db['db'],
            config.supra_db['user'],
            config.supra_db['pwd']
        ))
        cursor = conn.cursor()

        select_query = "SELECT *  FROM " + table
        cursor.execute(select_query)
        results = cursor.fetchall()
        result_list = [
            dict(zip([column[0] for column in cursor.description], row)) for row in results]
        return result_list

    except pyodbc.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

    finally:
        cursor.close()
        conn.close()

    return None


def get_select_tb_servicos_roteiro():
    try:
        conn = pyodbc.connect(db.get_connection_string(
            config.supra_db['server'],
            config.supra_db['db'],
            config.supra_db['user'],
            config.supra_db['pwd']
        ))
        cursor = conn.cursor()

        id_roteiro_controle_projeto = 37
        name_roteiro_controle_projeto = 'Controle de Projeto'
        select_query =  """ 
                            SELECT * FROM [SUPRA].[dbo].[TB_SERVICO] s  inner
                                join TB_ROTEIRO r on r.id_roteiro = s.roteiro  
                                where   id_roteiro = """+ str(id_roteiro_controle_projeto) +""" 
                                    and r.roteiro = '"""+ name_roteiro_controle_projeto +"""'
                        """
        cursor.execute(select_query)
        results = cursor.fetchall()
        result_list = [
            dict(zip([column[0] for column in cursor.description], row)) for row in results]
        return result_list

    except pyodbc.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

    finally:
        cursor.close()
        conn.close()

    return None



def insert_query_generic(table_name, columns, insert_values, id_column):
    try:
        conn = pyodbc.connect(db.get_connection_string(
            config.supra_db['server'],
            config.supra_db['db'],
            config.supra_db['user'],
            config.supra_db['pwd']
        ))
        cursor = conn.cursor()

        # Construindo a consulta de inserção dinamicamente
        columns_str = ', '.join(f'[{col}]' for col in columns)
        placeholders = ', '.join('?' for _ in columns)
        
        insert_query = f"""
            INSERT INTO [SUPRA].[dbo].[{table_name}] 
            (
                {columns_str}
            ) 
            OUTPUT INSERTED.[""" + id_column + """] 
            VALUES (
                """ + placeholders +"""
            )
        """

        cursor.execute(insert_query, insert_values)
        inserted_id = cursor.fetchone()[0] 
        conn.commit()
        return inserted_id 
    except pyodbc.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        cursor.close()
        conn.close()
        
def update_query_generic(table_name, columns, values, id_column, id_item):
    try:
        conn = pyodbc.connect(db.get_connection_string(
            config.supra_db['server'],
            config.supra_db['db'],
            config.supra_db['user'],
            config.supra_db['pwd']
        ))
        cursor = conn.cursor()

        # Construindo a cláusula SET dinamicamente
        set_clause = ', '.join(f'[{col}] = ?' for col in columns)

        # Construindo a query de atualização
        query = f"""
            UPDATE [SUPRA].[dbo].[{table_name}]
            SET {set_clause}
            WHERE [{id_column}] = ?
        """

        cursor.execute(query, values + (id_item,))
        
        conn.commit()
        if cursor.rowcount == -1 or cursor.rowcount > 0:
            return id_item
        else:
            return cursor.rowcount

    except pyodbc.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
        
def checkLineExists(values):
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
            SELECT * FROM [cp_documento]
            WHERE 
            id_cp_contrato = '""" + str(values["id_cp_contrato"]) +"""'
            AND observacao = '""" + str(values["observacao"]) +"""'
            AND numero_sei = '""" + str(values["numero_sei"]) +"""'
            AND documento_sei = '""" + str(values["documento_sei"]) +"""'
            AND processo_sei = '""" + str(values["processo_sei"]) +"""'
            AND origem = '""" + str(values["origem"]) +"""'
            AND destino = '""" + str(values["destino"]) +"""'
            AND assunto = '""" + str(values['assunto']) +"""'
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
        




def getConfigConn():
    return pyodbc.connect(db.get_connection_string(
            config.supra_db['server'],
            config.supra_db['db'],
            config.supra_db['user'],
            config.supra_db['pwd']
        ))
    



