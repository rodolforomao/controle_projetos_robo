
import model.excel as excel
import model.sei as sei

import model.supra as supra
import util.file as files_class

import config.config as config

def executar():
    
    files = files_class.listar_planilhas()
    
    for file in files:
        if '~$' not in file and 'xls' in file:
            if config.MIGRACAO_DB:
                list_documento_sei = excel.extrair_sei(file)
                if list_documento_sei is not None and len(list_documento_sei) > 0:
                    supra.migracao_dados(list_documento_sei, file)
            
            if config.DOWNLOAD_sei or config.VALIDACAO_SEI:
                list_documento_sei = excel.extrair_sei(file, False)
                if list_documento_sei is not None and len(list_documento_sei) > 0:
                    sei.executar(list_documento_sei, file)
                    # Adicionar informações no banco de dados, caso ela não exista
                
    
    
