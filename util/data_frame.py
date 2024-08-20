import util.string_format as string_format

def get_column(df, target_name, get_first_valid = False):
    target_name_normalized = string_format.normalize_text(target_name)
    
    for column in df.columns:
        normalized_column = string_format.normalize_text(column)
        if target_name_normalized in normalized_column:
            if get_first_valid:
                valid_values = df[column].dropna()
                if not valid_values.empty:
                    return valid_values.iloc[0]
            else:
                return df[column]
    
    print(f"Column similar to '{target_name}' not found.")
    return None