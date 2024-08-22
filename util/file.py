import shutil
import os
import time

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