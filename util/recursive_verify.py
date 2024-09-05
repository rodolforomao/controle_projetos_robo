import pandas as pd

def get_data_key(row, key):
    km_inicial = row.get(key)
    if km_inicial is not None:
        return km_inicial
    return None


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

