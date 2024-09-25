import shutil
import os
import time

from pathlib import Path

import model.supra as supra

import util.string_format as string_format

def move(file, target_file, max_retries=10, wait_time=1):
    retries = 0
    while retries < max_retries:
        try:
            if os.path.exists(target_file):
                target_file = get_unique_file_name(target_file)
                print(f"Target file already exists. Renaming to {target_file}")

            shutil.move(file, target_file)
            
            if not os.path.exists(file) and os.path.exists(target_file):
                print(f"File moved successfully from {file} to {target_file}.")
                return True

        except Exception as e:
            print(f"Error: {e}. Retrying in {wait_time} seconds...")
            
        retries += 1
        time.sleep(wait_time)
            
    return False


def get_unique_file_name(file_path):
    base, ext = os.path.splitext(file_path)
    counter = 1
    new_file_path = file_path

    while os.path.exists(new_file_path):
        new_file_path = f"{base}_{counter}{ext}"
        counter += 1
    
    return new_file_path


import os

def listar_planilhas():
    return os.listdir( os.path.join(os.getcwd(), 'files'))

def checkAndCreateFolder(target_dir):
    directory_path = os.path.dirname(target_dir)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    return Path(target_dir)

def checkAndCreateOnlyFolder(target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    return Path(target_dir)
    

def checkFileExist(prefix, file, target_dir = './files/sei_downloaded'):
    numero_contrato = supra.get_contract(file)
    numero_contrato = string_format.normalizar_texto(numero_contrato) + '/'
    target_dir += '/' + numero_contrato
    target_dir = Path(target_dir)
    checkAndCreateOnlyFolder(target_dir)
    existing_files = set(os.path.join(target_dir, f) for f in os.listdir(target_dir))
    for existing_file in existing_files:
        if prefix in existing_file:
            return True
    return False

