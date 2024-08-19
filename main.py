
import controller.browser_util as browser_util
import controller.principal as principal


repeat = True

while repeat:
    try:
        try:
            print('Main - Iniciando processo')
            
            principal.executar()           
            
            
            print('Main - COAC - Robo: Finalizado processo')
            
        except Exception as e:
            #browser_util.closeAllChromeInstances()
            print(e)
            
    except Exception as e:
        print(e)
        print('Exception main 1: Main - Dici - Robo: Finalizado processo com ERRO')
        
    input("Pressione Enter para sair...")

