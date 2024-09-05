import re
import pandas as pd

def verificarDuplicidadeDeFases(df):
    pattern = re.compile(r'estudos\s*hidrol[oó]gicos\s*[/\\]\s*hidráu[li]ico', re.IGNORECASE)
    def contains_pattern(text):
        return bool(pattern.search(text))
    matching_rows = df[df['FASE'].apply(contains_pattern)]
    new_rows = []
    for _, row in matching_rows.iterrows():
        new_row_1 = row.copy()
        new_row_1['FASE'] = pattern.sub('Estudos Hidrológicos', row['FASE'])

        new_row_2 = row.copy()
        new_row_2['FASE'] = pattern.sub('Estudos Hidráulico', row['FASE'])

        new_rows.append(new_row_1)
        new_rows.append(new_row_2)

    df = df.drop(matching_rows.index).reset_index(drop=True)
    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True).sort_index().reset_index(drop=True)

    return df
