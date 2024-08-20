
import model.excel as excel
import model.sei as sei

import model.supra as supra
import model.files as files_class

def executar():
    
    files = files_class.listar_planilhas()
    
    for file in files:
        list_documento_sei = excel.extrair_sei(file)
        if list_documento_sei is not None and len(list_documento_sei) > 0:
            supra.migracao_dados(list_documento_sei, file)
        
        list_documento_sei = excel.extrair_sei(file, False)
        if list_documento_sei is not None and len(list_documento_sei) > 0:
            print('')
            sei.executar(list_documento_sei)
            # Adicionar informações no banco de dados, caso ela não exista
            
    
    
