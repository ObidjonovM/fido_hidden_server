from . import model_utils as utls


def last_pk_value(table_name):
    col_names = utls.get_column_names(table_name)
    pk_col = col_names[0]
    sql = f'SELECT log_id FROM {table_name} ORDER BY log_id DESC LIMIT 1'
    result = utls.send_to_db(sql, None, True)

    if not result['success']:
        return {pk_col : -1}

    if len(result['data']) == 0:
        return {pk_col : 0}
    
    return {pk_col : result['data'][0][0]}


def insert(table_name, info, generate_pk=True):
    if generate_pk:
        pk, val = last_pk_value(table_name).popitem()       # getting the last value of PK column
        sql = f'INSERT INTO {table_name} ({pk}, '
        values = f'VALUES ({int(val) + 1}, '
    else:
        sql = f'INSERT INTO {table_name} ('
        values = f'VALUES ('

    for key in info.keys():
        sql += key + ', '
        values += f'%({key})s, '

    sql = sql[:-2] + ')'
    values = values[:-2] + ')'
    sql = sql + values
    return utls.send_to_db(sql, info, False)


def get(table_name, rec_dict):
    col_names = utls.get_column_names(table_name)
    cpy_rec_dict = rec_dict.copy()
    k, v = cpy_rec_dict.popitem()
    sql = f'SELECT * FROM {table_name} WHERE {k} = %({k})s'
    result = utls.send_to_db(sql, {k : v}, True)

    if result['success'] and len(result['data']) > 0:
        result['data'] = utls.keyval_tuples2dict(col_names, result['data'][0])

    return result


def get_last(table_name, target_col, rec_dict):
    col_names = utls.get_column_names(table_name)
    cpy_rec_dict = rec_dict.copy()
    k, v = cpy_rec_dict.popitem()
    sql = f'SELECT * FROM {table_name} WHERE {k} = %({k})s ORDER BY {target_col} DESC LIMIT 1'
    result = utls.send_to_db(sql, {k : v}, True)

    if result['success'] and len(result['data']) > 0:
        result['data'] = utls.keyval_tuples2dict(col_names, result['data'][0])

    return result


def get_all_device_records(table_name, device_info):
    col_names = utls.get_column_names(table_name)
    cpy_device_info = device_info.copy()
    k, v = cpy_device_info.popitem()
    sql = f'SELECT * FROM {table_name} WHERE {k} = %({k})s '
    result = utls.send_to_db(sql, {k : v}, True)

    if result['success']:
        result['data'] = utls.list_tuples2tuple_lists(result['data'])
        result['data'] = utls.keyval_tuples2dict(col_names, result['data'])

    return result


def get_all_in_date(table_name, datetime_col, device_info, date_range):
    col_names = utls.get_column_names(table_name)
    cpy_device_info = device_info.copy()
    k, v = cpy_device_info.popitem()
    sql = f'SELECT * FROM {table_name} WHERE {k} = %({k})s AND '
    sql += f'{datetime_col} BETWEEN %(start)s AND %(end)s'
    
    result = utls.send_to_db(
            sql, 
            {k : v, 'start' : date_range['start'], 'end' : date_range['end']}, 
            True
        )

    if result['success']:
        result['data'] = utls.list_tuples2tuple_lists(result['data'])
        result['data'] = utls.keyval_tuples2dict(col_names, result['data'])

    return result


def update(table_name, prim_col, info):
    sql = f'UPDATE {table_name} SET '
    for key in info.keys():
        if key != prim_col:
            sql += f'{key} = %({key})s, '

    sql = sql[:-2] + f' WHERE {prim_col} = %({prim_col})s'

    return utls.send_to_db(sql, info, False)


def update_by_filter(table_name, filter_cols, info):
    sql = f'UPDATE {table_name} SET '
    for key in info.keys():
        sql += f'{key} = %({key})s, '

    sql = sql[:-2] + ' WHERE '

    for col in filter_cols:
        sql += f'{col} = %({col})s AND '

    sql = sql[:-5]

    return utls.send_to_db(sql, info, False)