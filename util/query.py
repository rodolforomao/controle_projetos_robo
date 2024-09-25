
def checkIsNull(column_value, value, column_query = None):
    if column_query is None:
        column_query = column_value
    query = ""
    if value[column_value] is None:
        query +=  """    
            AND """+ column_query +""" is null 
        """
    else:
        query +=  """    
            AND """+ column_query +""" = '""" + str(value[column_value]).replace("'", "''") +"""'
        """
    return query


def get_raw_query(query, values):
    for value in values:
        # Check if the value is a string, and quote it for SQL syntax
        if isinstance(value, str):
            query = query.replace('?', f"'{value}'", 1)
        elif value is None:
            query = query.replace('?', 'NULL', 1)
        else:
            query = query.replace('?', str(value), 1)
    return query