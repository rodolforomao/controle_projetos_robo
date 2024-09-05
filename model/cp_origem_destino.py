
import util.string_format as string_format

import model.db as db

TABLE_NAME = 'cp_origem_destino'
COLUMN_ID = 'id_origem_destino'

NAME_COLUMN = 'nome'
    
def get_status(value):
    return string_format.get_item(value, get_db_all_items(),NAME_COLUMN)
    
def get_db_all_items():
    return db.get_select(TABLE_NAME)