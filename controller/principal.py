
import model.excel as excel
import model.sei as sei

def executar():
    
    list_documento_sei = excel.extrair_sei()
    
    if list_documento_sei is not None and len(list_documento_sei) > 0:
        sei.executar(list_documento_sei)
        
    
    
