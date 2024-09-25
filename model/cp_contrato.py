import pyodbc
import model.db as db

TABLE_NAME = 'cp_contrato'
COLUMN_ID = 'id_cp_contrato'

def get_columns():
    return (
    #   'id_contrato_obra',
    #   'id_siac_contrato',
        'contrato',
    )

def insertCpContrato(numero_contrato):
    
    if numero_contrato is None:
        return None
    
    values = (
            numero_contrato, # ,[contrato]
    )
    
    return db.insert_query_generic(TABLE_NAME, get_columns() ,values, COLUMN_ID)
  

def getIdCpContratoByIdContrato(numero_contrato):
    
    conn = db.getConfigConn()
    cursor = conn.cursor()
    id_cp_contrato = None
    try:
        
        select_query = ''' SELECT '''+  COLUMN_ID +''' FROM '''+  TABLE_NAME +''' WHERE contrato = ? '''

        cursor.execute(select_query, numero_contrato)
        result = cursor.fetchone()
        
        if result is None:
            id_cp_contrato = insertCpContrato(numero_contrato)
        else:
            id_cp_contrato = result.id_cp_contrato
            
        return id_cp_contrato
    except pyodbc.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        cursor.close()
        conn.close()

    return None


def getIdByContrato(numero_contrato):
    
    conn = db.getConfigConn()
    cursor = conn.cursor()
    try:
        select_query = '''
        select * from
        (
            SELECT iif(id_siac_contrato IS NULL, 0, 1) AS [exists], contrato, id_siac_contrato, NULL AS id_contrato_obra
            FROM [SUPRA].[dbo].TB_SIAC_CONTRATO
            WHERE contrato LIKE ?
            UNION
            SELECT iif(id_contrato_obra IS NULL, 0, 1) AS [exists], contrato, NULL AS id_siac_contrato, id_contrato_obra
            FROM TB_CONTRATO_OBRA
            WHERE contrato LIKE ?
        ) tabela
            order by id_siac_contrato desc
        '''

        # Execute the query with parameter
        cursor.execute(select_query, (f'%{numero_contrato}%', f'%{numero_contrato}%'))
        result = cursor.fetchone()
        
        if result is not None:
            columns = [column[0] for column in cursor.description]
            
            row_dict = dict(zip(columns, result))
            
            id_siac_contrato = row_dict.get('id_siac_contrato')
            id_contrato_obra = row_dict.get('id_contrato_obra')
            
            supra = False
            siac = False
            if id_siac_contrato is not None:
                id = id_siac_contrato
                siac = True
            if id_contrato_obra is not None:
                id = id_contrato_obra
                supra = True
            
            return id, siac, supra
    except pyodbc.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        cursor.close()
        conn.close()

    return None

def get_supra_contrato(numero_contrato):
    if numero_contrato:
        try:
            
            #id_contrato, siac, supra = getIdByContrato(numero_contrato)
            
            id_cp_contrato = getIdCpContratoByIdContrato(numero_contrato)
            
            return id_cp_contrato

        except pyodbc.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
        
    return None