import pandas as pd
from rapidfuzz import fuzz, process

def get_data_key(row, key, fuzzy = False, ratio = 90):
    
    if fuzzy == True:
        km_inicial = get_data_key_fuzzy(row,key, ratio)
    else:
        km_inicial = row.get(key)
    
    return km_inicial


def get_data_key_fuzzy(row, correct_column, ratio = 90):
    #matches = process.extractOne(correct_column, row.index, scorer=process.fuzz.ratio)
    matches = process.extractOne(correct_column, row.index, scorer=fuzz.ratio)

    if matches and matches[1] >= ratio:
        best_match = matches[0]
        value = row[best_match]
    else:
        value = None

    return value


def get_data_value(container, keys_or_indices):
    if not keys_or_indices:
        return container

    current_key_or_index = keys_or_indices[0]

    if isinstance(container, (dict, pd.Series)):
        value = container.get(current_key_or_index, None)
    
    elif isinstance(container, (list, tuple, str)):
        try:
            index = int(current_key_or_index) if isinstance(current_key_or_index, (int, str)) and str(current_key_or_index).isdigit() else None
            value = container[index] if index is not None else None
        except (IndexError, ValueError, TypeError):
            return None
    
    elif isinstance(container, set):
        value = current_key_or_index if current_key_or_index in container else None
    
    else:
        return None

    if value is None or len(keys_or_indices) == 1:
        return value

    return get_data_value(value, keys_or_indices[1:])

