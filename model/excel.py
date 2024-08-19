import pandas as pd
import re

def extrair_sei():
    file_path = 'files/SEI_DNIT - 16453831 - Despacho (DNIT) - Copia.xlsx'
    # file_path = 'files/SEI_DNIT - 16453831 - Despacho (DNIT).xlsx'

    try:
        df = pd.read_excel(file_path, sheet_name='Table 1')
    except ValueError:
        try:
            df = pd.read_excel(file_path, sheet_name='Tabela 1')
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return pd.DataFrame()

    if 'TERMO DE ACEITE' in df.columns:
        def extract_sei_number(text):
            if text is None or pd.isna(text):
                return None
            try:
                match = re.search(r'\b\d{7}\b', str(text))
                if match:
                    return match.group()
                return None
            except Exception as e:
                print(f"Erro na extração do SEI: {e}")
                return None

        df['SEI Number'] = df['TERMO DE ACEITE'].apply(extract_sei_number)

        df['Row Number'] = df.index + 2  # Soma 2 para ajustar ao número da linha no Excel (conta 1 para header e 1 para índice 0)

        filtered_df = df.dropna(subset=['SEI Number'])

        print(filtered_df)
        return filtered_df
    else:
        return pd.DataFrame()  # Retorna um DataFrame vazio se a coluna não existir
