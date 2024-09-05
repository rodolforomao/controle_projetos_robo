import re

def get_sei_document(text):
    match = re.search(r'\b\d{7}\b', str(text))
    if match:
        return match.group()
    return None


def get_numero_sei(termo_aceite, rap):
    num_sei = get_sei_document(termo_aceite)
    if num_sei is None:
        num_sei = get_sei_document(rap)
    return num_sei