import pyodbc

import model.db as db

import config.config as config

def get_connection_string(server = 'localhost', database = 'SUPRA', username = 'teste', password = 'Ab1234567'):
    return f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'


def get_supra_origem_destino():
    return get_select('cp_origem_destino')


def get_supra_tipo_documento():
    return get_select('cp_tipo')



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
            INSERT INTO [SUPRA].[dbo].[cp_documento] 
            (
                
                [id_contrato_obra],
                [numero_sei],
                [data_encaminhamento],
                [origem],
                [destino],
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
            VALUES (
                ?,  -- [id_contrato_obra],
                ?, -- [numero_sei],
                ?, -- [data_encaminhamento],
                ?, -- [origem],
                ?, -- [destino],
                ?, -- [assunto],
                ?, -- [observacao],
                ?, -- [id_usuario],
                ?, -- [ultima_alteracao],
                ?, -- [id_tipo],
                ?, -- [processo_sei],
                ?, -- [documento_sei],
                ?, -- [publicar],
                ?, -- [data_publicar],
                ? -- [id_usuario_nao_publicar]
                )
        """

        cursor.executemany(insert_query, insert_values)
        conn.commit()

        # Limpa a lista após o commit
        insert_values.clear()

    except pyodbc.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        cursor.close()
        conn.close()
        
        
def get_supra_contrato(numero_contrato):
    if numero_contrato:
        try:
            # Conectando ao banco de dados
            conn = pyodbc.connect(db.get_connection_string(
                config.supra_db['server'],
                config.supra_db['db'],
                config.supra_db['user'],
                config.supra_db['pwd']
            ))
            cursor = conn.cursor()

            # Executando um SELECT com parâmetros para evitar injeção de SQL
            select_query = "SELECT id_contrato_obra as id FROM TB_CONTRATO_OBRA WHERE contrato LIKE ?"
            cursor.execute(select_query, '%' + numero_contrato + '%')

            # Obtendo o primeiro resultado
            result = cursor.fetchone()
            if result:
                return result.id  # Retorna o ID

        except pyodbc.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

        finally:
            cursor.close()
            conn.close()

    return None