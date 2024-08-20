

def get_connection_string(server = 'localhost', database = 'SUPRA', username = 'teste', password = 'Ab1234567'):
    return f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
