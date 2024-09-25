import model.db as db

import util.string_format as string_format

TABLE_NAME = 'tb_servicos'


def get_br_from_contrato(id_cp_contato):
    data = get_db_item_id(id_cp_contato)
    if len(data) > 0:
        for item in data:
            return item['br']
    return False

def get_db_item_id(id_cp_contato):
    query = '''
             DECLARE @contrato varchar(max);

            SELECT 
                @contrato = contrato
            FROM [SUPRA].[dbo].[cp_contrato]
                WHERE id_cp_contrato = ''' + str(id_cp_contato) + '''
                    select distinct * from
                    (
                                SELECT br
                                FROM TB_CONTRATO_OBRA 
                                WHERE contrato like '%' + @contrato + '%' 
                                AND @contrato is not null

                                UNION ALL

                                SELECT TOP 1 rodovia br
                                FROM tb_siac_segmento
                                WHERE @contrato IS NOT NULL 
                                AND contrato = @contrato
                    ) tabela;
        '''
    return db.get_select_query(query)


