import math

import model.db as db
import util.string_format as string_format

TABLE_NAME = 'cp_status'
COLUMN_ID = 'id_status'
NAME_COLUMN = 'nome'


def get_status_converting_status(value):
    if isinstance(value, float) and math.isnan(value):
        return None
    new_value = None
    get_one = True
    precisao = 90 # aprovado != naoaprovado
    if string_format.get_item(value, [{ NAME_COLUMN: 'Aprovado'}],NAME_COLUMN, get_one, precisao):
        new_value = 'Termo de Aceite'
    return get_status(new_value)
    
    
def get_db_all_items():
    return db.get_select(TABLE_NAME)

def get_status(value):
    return string_format.get_item(value, get_db_all_items(),NAME_COLUMN)

def get_id_status(value):
    dados = get_status(value)
    
    if len(dados) > 0:
        for item in dados:
            return item[COLUMN_ID]
    return False

