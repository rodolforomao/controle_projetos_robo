
import os

def listar_planilhas():
    return os.listdir( os.path.join(os.getcwd(), 'files'))