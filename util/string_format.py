def normalize_text(name):
    # Remove spaces, convert to lowercase, and remove accents
    name = name.strip().replace(" ", "").lower()
    name = remove_accents(name)
    return name

def remove_accents(input_str):
    # Function to remove accents from characters
    import unicodedata
    return ''.join(
        (c for c in unicodedata.normalize('NFD', input_str) if unicodedata.category(c) != 'Mn')
    )
