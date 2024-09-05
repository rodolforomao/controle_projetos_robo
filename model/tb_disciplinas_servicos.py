import model.db as db

import util.string_format as string_format

COLUMN_ID = "id_servico"
COLUMN_NAME = "servico"

TIPO_PROJETO_ESTUDOS_HIDROLOGICO_FULL = 'Estudo Hidrológico'
TIPO_PROJETO_ESTUDOS_HIDROLOGICO = 'HIDROLOGIA'

TIPO_PROJETO_ESTUDOS_TRAFEGO_FULL = 'Estudos de Tráfego'
TIPO_PROJETO_ESTUDOS_TRAFEGO = 'Trafégo'

TIPO_PROJETO_ESTUDOS_INTERFERENCIAS = 'Interferências'

TIPO_PROJETO_ESTUDOS_CONTENCOES = 'Contenções'
TIPO_PROJETO_ESTUDOS_CONTENCAO = 'Contenção'

TIPO_PROJETO_OAE = 'OAE'
TIPO_PROJETO_OAE_existente_restaura = 'restaura'

TIPO_PROJETO_OAE_EXISTENTE = 'OAE Existente'
TIPO_PROJETO_OAE_NOVA = 'OAE nova'

TIPO_PROJETO_ESTUDOS_PAVIMENTACAO = 'Pavimentação'
TIPO_PROJETO_ESTUDOS_REVESTIMENTO = 'Revestimento'

TIPO_PROJETO_ESTUDOS_RESTAURACAO_FULL = 'Restauração do paVimento'
TIPO_PROJETO_ESTUDOS_RESTAURACAO = 'Restauração'

TIPO_PROJETO_PAISAGISMO = 'Paisagismo'
TIPO_PROJETO_OBRAS_COMPLEMENTARES = 'Obras Complementares'

def get_table_name():
    return 'tb_servicos'

def get_db_all_items():
    return db.get_select_tb_servicos_roteiro()

def get_id_tipo_disciplina(value):
    dados = get_tipo_disciplina(value)
    if len(dados) > 0:
        for item in dados:
            return item[COLUMN_ID]
    
    if string_format.comparar_strings(TIPO_PROJETO_ESTUDOS_PAVIMENTACAO, value,95, True):
        dados = get_tipo_disciplina(TIPO_PROJETO_ESTUDOS_REVESTIMENTO)
        if len(dados) > 0:
            for item in dados:
                return item[COLUMN_ID]
            
    if string_format.comparar_strings(TIPO_PROJETO_ESTUDOS_RESTAURACAO_FULL, value,95, True):
        dados = get_tipo_disciplina(TIPO_PROJETO_ESTUDOS_RESTAURACAO)
        if len(dados) > 0:
            for item in dados:
                return item[COLUMN_ID]
    
    if string_format.comparar_strings(TIPO_PROJETO_ESTUDOS_HIDROLOGICO_FULL, value,95):
        dados = get_tipo_disciplina(TIPO_PROJETO_ESTUDOS_HIDROLOGICO)
        if len(dados) > 0:
            for item in dados:
                return item[COLUMN_ID]
    
    if string_format.comparar_strings(TIPO_PROJETO_ESTUDOS_TRAFEGO_FULL, value,95):
        dados = get_tipo_disciplina(TIPO_PROJETO_ESTUDOS_TRAFEGO)
        if len(dados) > 0:
            for item in dados:
                return item[COLUMN_ID]
    
    if string_format.compare_item_includes(value, TIPO_PROJETO_ESTUDOS_INTERFERENCIAS):
        dados = get_tipo_disciplina(TIPO_PROJETO_ESTUDOS_INTERFERENCIAS)
        if len(dados) > 0:
            for item in dados:
                return item[COLUMN_ID]
    
    if string_format.comparar_strings(TIPO_PROJETO_ESTUDOS_CONTENCOES, value,85, True):
        dados = get_tipo_disciplina(TIPO_PROJETO_ESTUDOS_CONTENCOES)
        if len(dados) > 0:
            for item in dados:
                return item[COLUMN_ID]
            
    if string_format.compare_item_includes(value, TIPO_PROJETO_ESTUDOS_CONTENCAO):
        dados = get_tipo_disciplina(TIPO_PROJETO_ESTUDOS_CONTENCAO)
        if len(dados) > 0:
            for item in dados:
                return item[COLUMN_ID]
            
    if string_format.compare_item_includes(value, TIPO_PROJETO_OAE, True):
        if string_format.compare_item_includes(value, TIPO_PROJETO_OAE_existente_restaura, True):
            dados = get_tipo_disciplina(TIPO_PROJETO_OAE_EXISTENTE)
            if len(dados) > 0:
                for item in dados:
                    return item[COLUMN_ID]
        else:
            if string_format.compare_item_includes(value, TIPO_PROJETO_OAE):
                dados = get_tipo_disciplina(TIPO_PROJETO_OAE_NOVA)
                if len(dados) > 0:
                    for item in dados:
                        return item[COLUMN_ID]
    
    if string_format.comparar_strings(TIPO_PROJETO_PAISAGISMO, value,85, True):
        dados = get_tipo_disciplina(TIPO_PROJETO_OBRAS_COMPLEMENTARES)
        if len(dados) > 0:
            for item in dados:
                return item[COLUMN_ID]
    
    return False

def get_tipo_disciplina(value, fuzzy = True):
    if fuzzy:
        return string_format.get_item(value, get_db_all_items(),COLUMN_NAME)
    
    return string_format.get_item_compare(value, get_db_all_items(),COLUMN_NAME)
