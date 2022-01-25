import psycopg2 as pg2
from sys import exc_info

from hidden_server import config
 

def get_column_names(table_name):
    conn = None
    cur = None
    names_list = None
    names = None

    try:
        conn = pg2.connect(config.db_credentials)
        cur = conn.cursor()
        cur.execute('''
                SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME=%(table_name)s ORDER BY ORDINAL_POSITION''',
                {'table_name' : table_name})
        names_list = cur.fetchall()

    except pg2.Error as e:
        print(e)
        # TODO: the error needs to be saved to log table

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    if names_list:
        names = tuple(name[0] for name in names_list)

    return names


def keyval_tuples2dict(keys_tuple, vals_tuple):
    return dict(zip(keys_tuple, vals_tuple))


def list_tuples2tuple_lists(list_tuples):
    """
    INPUT: list_tuples - list of tuples where the length of each tuple should be greater than 1.
    RETURNS: It returns tuple where each element of it is a list which contains elements of tuples at the input.
    EXAMPLE:
    input: [(1, 'Azamat', 'Tuychiev', 'programmer'), (2, 'Ganisher', 'Ganiev', 'analitik'), (3, 'Barak', 'Obama', 'stajor')]
        output: ([1,2,3], ['Azamat','Ganisher','Barak'], ['Tuychiev','Ganiev','Obama'], ['programmer','analitik','stajor']) 
    """
    if list_tuples == []:
        return tuple()

    list_of_lists = []
    tuple_len = len(list_tuples[0])
    for _ in range(tuple_len):
        list_of_lists.append([])
    
    for tup in list_tuples:
        for i in range(tuple_len):
            list_of_lists[i].append(tup[i])

    return tuple(list_of_lists)


def execute_query(query_params):
    conn = None
    cur = None
    success = False
    data = dict()
    error_name = ''
    error_desc = ''
    error_line_num = 0

    try:
        conn = pg2.connect(config.db_credentials)
        cur = conn.cursor()
        cur.execute(query_params['sql'], query_params['sql_params'])
        if query_params['fetchable']:
            data = cur.fetchall()
        else:
            conn.commit()
        success = True

    except:
        if not query_params['fetchable'] and conn:
            conn.rollback()
        exc_class, exc_value, exc_traceback = exc_info()
        error_name = exc_class.__name__
        error_desc = str(exc_value) + ' :: ' + create_func_input(**query_params)
        error_line_num = exc_traceback.tb_lineno 

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    return {
    'success' : success,
    'data' : data,
    'error_name' : error_name,
    'error_desc' : error_desc,
        'error_line_num' : error_line_num
    }
    

def create_func_input(**kwargs):
    desc = 'INPUTS :'
    for k,v in kwargs.items():
        desc += f' {k} = {str(v)};'

    return desc


def send_to_db(sql, info, fetchable):
    return execute_query({
    'sql' : sql,
    'sql_params' : info,
    'fetchable' : fetchable
    })