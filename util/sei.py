import re

def get_sei_document(text):
    match = re.search(r'\b\d{7}\b', str(text))
    if match:
        return match.group()
    return None