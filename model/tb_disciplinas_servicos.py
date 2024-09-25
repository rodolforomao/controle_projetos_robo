import logging
import math
import pandas as pd

import model.db as db

import util.string_format as string_format
import util.log as log

COLUMN_ID = "id_servico"
COLUMN_NAME = "servico"

TIPO_PROJETO_ESTUDOS_HIDROLOGICO_FROM = 'Estudo Hidrológico'
TIPO_PROJETO_HIDROLOGICOS_FULL = 'Hidrológicos'
TIPO_PROJETO_ESTUDOS_HIDROLOGICO_TO = 'HIDROLOGIA'

TIPO_PROJETO_ESTUDOS_TRAFEGO_FROM = 'Estudos de Tráfego'
TIPO_PROJETO_ESTUDOS_TRAFEGO_TO = 'Trafégo'

TIPO_PROJETO_ESTUDOS_INTERFERENCIAS = 'Interferências'

TIPO_PROJETO_ESTUDOS_CONTENCOES = 'Contenções'
TIPO_PROJETO_ESTUDOS_CONTENCAO = 'Contenção'

TIPO_PROJETO_OAE_FROM = 'OAE'
TIPO_PROJETO_OAE_2 = 'Obras-de-Arte Especia'

TIPO_PROJETO_OAE_existente_restaura = 'restaura'

TIPO_PROJETO_OAE_EXISTENTE_TO = 'OAE Existente'
TIPO_PROJETO_OAE_NOVA_TO = 'OAE nova'

TIPO_PROJETO_ESTUDOS_PAVIMENTACAO = 'Pavimentação'
TIPO_PROJETO_ESTUDOS_REVESTIMENTO = 'Revestimento'

TIPO_PROJETO_ESTUDOS_RESTAURACAO_FULL = 'Restauração do paVimento'
TIPO_PROJETO_ESTUDOS_RESTAURACAO = 'Restauração'

TIPO_PROJETO_PAISAGISMO_FROM = 'Paisagismo'
TIPO_PROJETO_OBRAS_COMPLEMENTARES_TO = 'Obras Complementares'

TIPO_PROJETO_PLANO_SONDAGEM_FROM = 'Plano de Sondagem'
TIPO_PROJETO_PLANO_SONDAGEM_TO = 'Fundação'

TIPO_PROJETO_GEOLOGICO = 'geologico'
TIPO_PROJETO_TOPOGRAFICO = 'topografico'
TIPO_PROJETO_GEOTECNICO = 'geotecnico'
TIPO_PROJETO_AMBIENTAIS_TO = 'ambientais'
TIPO_PROJETO_AMBIENTAL_FROM = 'ambiental'

TIPO_PROJETO_TRACADO_FROM = 'traçado'
TIPO_PROJETO_TRACADO_TOPOGRAFICO_TO = 'topografico'

TIPO_PROJETO_URB_FROM = 'urbanismo'
TIPO_PROJETO_PAIS = 'paisagismo'
TIPO_PROJETO_ARQ = 'arquitetura'
TIPO_PROJETO_ARQ_URB_OBRAS_COMPLEMENTARES_TO = 'Obras Complementares'

TIPO_PROJETO_DESAPROPRIACAO_RELATORIO_GENERICO_DE_VALORES = 'Relatório Genérico de Valores'
TIPO_PROJETO_CADASTRO_TECNICO_COMPLETO = 'Cadastro Técnico Completo'
TIPO_PROJETO_DESAPROPRIACAO_TO = 'desapropriação'
TIPO_PROJETO_REASSENTAMENTO = 'reassentamento'

TIPO_PROJETO_ORCAMENTO = 'orçamento'

TIPO_PROJETO_INTERFERENCIAS = 'orçamento'

TIPO_PROJETO_SUBLEITO_FROM = 'subleito'
TIPO_PROJETO_FUNDACAO_TO = 'fundação'

TIPO_PROJETO_SINALIZACAO = 'Sinalização'

TIPO_PROJETO_INTERSECCOES_1 = 'Intersecções'
TIPO_PROJETO_INTERSECCOES_2 = 'Interseções'


TIPO_PROJETO_ILUMINACAO_PUBLICA = 'Iluminação Pública'
TIPO_PROJETO_CONTRO_DE_CONTROLE_FROM = 'Centro de Controle'
TIPO_PROJETO_OBRAS_COMPLEMENTARES_TO = 'Obras Complementares'

TIPO_PROJETO_OAC_FROM = 'OAC'
TIPO_PROJETO_OAC_DB_TO = 'Drenagem/OAC'

COLUMN_SERVICO = 'servico'


def get_table_name():
    return 'tb_servicos'

def get_db_all_items():
    return db.get_select_tb_servicos_roteiro()

import util.log as log

def get_id_tipo_disciplina(row):
    value = row['DISCIPLINA']
    contrato = row['contrato']
    titulo = 'Tipo disciplina'
    if value is pd.NaT:
        return False
    
    if type(value) == float and math.isnan(value):
        return False
    
    dados = get_tipo_disciplina(value)
    if len(dados) > 0:
        for item in dados:
            log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + item[COLUMN_SERVICO], logging.INFO)
            return item[COLUMN_ID]
    
    if string_format.comparar_strings(TIPO_PROJETO_ESTUDOS_PAVIMENTACAO, value,95, True):
        tipo_procurado = TIPO_PROJETO_ESTUDOS_REVESTIMENTO
        dados = get_tipo_disciplina(tipo_procurado)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
            
    if string_format.comparar_strings(TIPO_PROJETO_ESTUDOS_RESTAURACAO_FULL, value,95, True):
        tipo_procurado = TIPO_PROJETO_ESTUDOS_RESTAURACAO
        dados = get_tipo_disciplina(tipo_procurado)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
    
    if string_format.comparar_strings(TIPO_PROJETO_ESTUDOS_HIDROLOGICO_FROM, value,95):
        tipo_procurado = TIPO_PROJETO_ESTUDOS_HIDROLOGICO_TO
        dados = get_tipo_disciplina(tipo_procurado)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
    
    if string_format.comparar_strings(TIPO_PROJETO_ESTUDOS_TRAFEGO_FROM, value,95):
        tipo_procurado = TIPO_PROJETO_ESTUDOS_TRAFEGO_TO
        dados = get_tipo_disciplina(tipo_procurado)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
    
    if string_format.compare_item_includes(value, TIPO_PROJETO_ESTUDOS_INTERFERENCIAS):
        tipo_procurado = TIPO_PROJETO_ESTUDOS_INTERFERENCIAS
        dados = get_tipo_disciplina(tipo_procurado)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
    
    if string_format.comparar_strings(TIPO_PROJETO_ESTUDOS_CONTENCOES, value,85, True):
        tipo_procurado = TIPO_PROJETO_ESTUDOS_CONTENCOES
        dados = get_tipo_disciplina(tipo_procurado)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
            
    if string_format.comparar_strings(TIPO_PROJETO_PLANO_SONDAGEM_FROM, value,90, True):
        tipo_procurado = TIPO_PROJETO_PLANO_SONDAGEM_TO
        dados = get_tipo_disciplina(tipo_procurado)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
            
    if string_format.compare_item_includes(value, TIPO_PROJETO_ESTUDOS_CONTENCAO):
        tipo_procurado = TIPO_PROJETO_ESTUDOS_CONTENCAO
        dados = get_tipo_disciplina(tipo_procurado)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
            
    if string_format.compare_item_includes(value, TIPO_PROJETO_OAE_FROM, True):
        if string_format.compare_item_includes(value, TIPO_PROJETO_OAE_existente_restaura, True):
            tipo_procurado = TIPO_PROJETO_OAE_EXISTENTE_TO
            dados = get_tipo_disciplina(tipo_procurado)
            if len(dados) > 0:
                for item in dados:
                    log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                    return item[COLUMN_ID]
        else:
            if string_format.compare_item_includes(value, TIPO_PROJETO_OAE_FROM):
                tipo_procurado = TIPO_PROJETO_OAE_NOVA_TO
                dados = get_tipo_disciplina(tipo_procurado)
                if len(dados) > 0:
                    for item in dados:
                        log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                        return item[COLUMN_ID]
    
    if string_format.comparar_strings(TIPO_PROJETO_PAISAGISMO_FROM, value,85, True):
        tipo_procurado = TIPO_PROJETO_OBRAS_COMPLEMENTARES_TO
        dados = get_tipo_disciplina(tipo_procurado)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
    
    if string_format.compare_item_includes(value, TIPO_PROJETO_GEOLOGICO, True):
        tipo_procurado = TIPO_PROJETO_GEOLOGICO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
            
    if string_format.compare_item_includes(value, TIPO_PROJETO_TOPOGRAFICO, True):
        tipo_procurado = TIPO_PROJETO_TOPOGRAFICO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
    
    if string_format.compare_item_includes(value, TIPO_PROJETO_GEOTECNICO, True):
        tipo_procurado = TIPO_PROJETO_GEOTECNICO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
    
    if string_format.compare_item_includes(value, TIPO_PROJETO_AMBIENTAIS_TO, True):
        tipo_procurado = TIPO_PROJETO_AMBIENTAIS_TO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
            
    if string_format.compare_item_includes(value, TIPO_PROJETO_TRACADO_FROM, True):
        tipo_procurado = TIPO_PROJETO_TRACADO_TOPOGRAFICO_TO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]

    if string_format.compare_item_includes(value, TIPO_PROJETO_URB_FROM, True) or string_format.compare_item_includes(value, TIPO_PROJETO_PAIS, True) or string_format.compare_item_includes(value, TIPO_PROJETO_ARQ, True):
        tipo_procurado = TIPO_PROJETO_ARQ_URB_OBRAS_COMPLEMENTARES_TO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
            
    if string_format.compare_item_includes(value, TIPO_PROJETO_DESAPROPRIACAO_TO, True) or string_format.compare_item_includes(value, TIPO_PROJETO_REASSENTAMENTO, True):
        tipo_procurado = TIPO_PROJETO_DESAPROPRIACAO_TO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
            
    if string_format.compare_item_includes(value, TIPO_PROJETO_ORCAMENTO, True):
        tipo_procurado = TIPO_PROJETO_ORCAMENTO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
    
    if string_format.compare_item_includes(value, TIPO_PROJETO_ESTUDOS_PAVIMENTACAO, True):
        tipo_procurado = TIPO_PROJETO_ESTUDOS_PAVIMENTACAO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
            
    if string_format.compare_item_includes(value, TIPO_PROJETO_ESTUDOS_INTERFERENCIAS, True):
        tipo_procurado = TIPO_PROJETO_ESTUDOS_INTERFERENCIAS
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
            
    if string_format.compare_item_includes(value, TIPO_PROJETO_ESTUDOS_HIDROLOGICO_FROM, True):
        tipo_procurado = TIPO_PROJETO_ESTUDOS_HIDROLOGICO_TO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]

    if string_format.compare_item_includes(value, TIPO_PROJETO_ESTUDOS_TRAFEGO_FROM, True):
        tipo_procurado = TIPO_PROJETO_ESTUDOS_TRAFEGO_TO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
 
    if string_format.compare_item_includes(value, TIPO_PROJETO_PLANO_SONDAGEM_FROM, True):
        tipo_procurado = TIPO_PROJETO_PLANO_SONDAGEM_TO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
    
    if string_format.compare_item_includes(value, TIPO_PROJETO_SUBLEITO_FROM, True):
        tipo_procurado = TIPO_PROJETO_FUNDACAO_TO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
            
    if string_format.compare_item_includes(value, TIPO_PROJETO_SINALIZACAO, True):
        tipo_procurado = TIPO_PROJETO_SINALIZACAO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
    
    if string_format.compare_item_includes(value, TIPO_PROJETO_INTERSECCOES_1,True) or string_format.compare_item_includes(value, TIPO_PROJETO_INTERSECCOES_2,True):
        tipo_procurado = TIPO_PROJETO_INTERSECCOES_1
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
    
    if string_format.compare_item_includes(value, TIPO_PROJETO_AMBIENTAL_FROM, True):
        tipo_procurado = TIPO_PROJETO_AMBIENTAIS_TO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
    
    if string_format.compare_item_includes(value, TIPO_PROJETO_ILUMINACAO_PUBLICA, True):
        tipo_procurado = TIPO_PROJETO_OBRAS_COMPLEMENTARES_TO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
            
    if string_format.compare_item_includes(value, TIPO_PROJETO_HIDROLOGICOS_FULL, True):
        tipo_procurado = TIPO_PROJETO_ESTUDOS_HIDROLOGICO_TO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
            
    if string_format.compare_item_includes(value, TIPO_PROJETO_OAE_2, True):
        if string_format.compare_item_includes(value, 'Restaura', True) or string_format.compare_item_includes(value, 'Manuten', True):
            tipo_procurado = TIPO_PROJETO_OAE_EXISTENTE_TO
            dados = get_tipo_disciplina(tipo_procurado, False, True, True)
            if len(dados) > 0:
                for item in dados:
                    log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                    return item[COLUMN_ID]
        else:
            tipo_procurado = TIPO_PROJETO_OAE_NOVA_TO
            dados = get_tipo_disciplina(tipo_procurado, False, True, True)
            if len(dados) > 0:
                for item in dados:
                    log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                    return item[COLUMN_ID]
    
    if string_format.compare_item_includes(value, TIPO_PROJETO_OAC_FROM, True):
        tipo_procurado = TIPO_PROJETO_OAC_DB_TO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
    
    if string_format.compare_item_includes(value, TIPO_PROJETO_CONTRO_DE_CONTROLE_FROM, True):
        tipo_procurado = TIPO_PROJETO_OBRAS_COMPLEMENTARES_TO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
    
    if string_format.compare_item_includes(value, TIPO_PROJETO_DESAPROPRIACAO_RELATORIO_GENERICO_DE_VALORES, True) or string_format.compare_item_includes(value, TIPO_PROJETO_CADASTRO_TECNICO_COMPLETO, True):
        tipo_procurado = TIPO_PROJETO_DESAPROPRIACAO_TO
        dados = get_tipo_disciplina(tipo_procurado, False, True, True)
        if len(dados) > 0:
            for item in dados:
                log.track(contrato, titulo + ': ' + value + ' convertido para -> ' + tipo_procurado, logging.WARNING)
                return item[COLUMN_ID]
    
    print('disciplina: ' + value)
    return False

def get_tipo_disciplina(value, fuzzy = True, normatizar = False, reverse = False):
    if fuzzy:
        return string_format.get_item(value, get_db_all_items(),COLUMN_NAME)
    
    return string_format.get_item_compare(value, get_db_all_items(),COLUMN_NAME, True, normatizar, reverse)
