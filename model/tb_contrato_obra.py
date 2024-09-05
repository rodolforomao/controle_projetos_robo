import model.db as db

import util.string_format as string_format

TABLE_NAME = 'tb_servicos'
COLUMN_ID_CAME = 'id_contrato_obra'


def get_br_from_contrato(id_contato_obra):
    data = get_db_item_id(id_contato_obra)
    if len(data) > 0:
        for item in data:
            return item['br']
    return False

def get_db_item_id(id_contato_obra):
    query = '''
            SELECT * FROM TB_CONTRATO_OBRA WHERE id_contrato_obra  = ''' + str(id_contato_obra) + '''
        '''
    return db.get_select_query(query)


