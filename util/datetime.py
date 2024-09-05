import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil import parser

def clean_date_time(date_str):
    cleaned_date = re.sub(r'[^\d/: ]', '', date_str)
    formato = "%d/%m/%Y"
    
    try:
        # Tenta converter com hora
        if ':' in cleaned_date:
            formato = "%d/%m/%Y %H:%M"
            return datetime.strptime(cleaned_date, formato)
        else:
            return datetime.strptime(cleaned_date, formato)
    except ValueError as e:
        #Correção de data
        if 'day is out of range for month' in str(e) + ' - Wrong date: ' + cleaned_date:
            # Se houver um erro, a data é inválida
            try:
                dia, mes, ano = map(int, cleaned_date.split('/'))
                # Corrige a data inválida
                while True:
                    try:
                        
                        data_corrigida = datetime(year=ano, month=mes, day=dia)
                        return data_corrigida
                        # print(f"Try fixing datetime: {data_corrigida}")
                        # return data_corrigida.strftime(formato) if not ':' in cleaned_date else data_corrigida.strftime(formato + " %H:%M")
                    except ValueError:
                        dia -= 1
                        if dia == 0:
                            mes -= 1
                            if mes == 0:
                                mes = 12
                                ano -= 1
                            dia = (datetime(ano, mes, 1) - timedelta(days=1)).day
            except ValueError:
                return None
    return None