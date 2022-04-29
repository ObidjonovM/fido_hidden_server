from . import model_utils as utls
from .. import config as cnfg


def last_pk_value(table_name):
    last_rec = cnfg.HIDDEN_DB[table_name].find_one(sort=[('_id', -1)])
    if last_rec == None:
        return 0

    return last_rec['_id']


@utls.execute_query
def insert(table_name, info, generate_pk=True):
    if generate_pk:
        last_id = last_pk_value(table_name)
        info['_id'] = last_id + 1
    res =  cnfg.HIDDEN_DB[table_name].insert_one(info)

    return res


@utls.execute_query
def get(table_name, rec_dict):
    res = dict()
    data = cnfg.HIDDEN_DB[table_name].find_one(rec_dict)
    if data != None:
        res = data

    return res



@utls.execute_query
def get_last(table_name, target_col, rec_dict):
    res = dict()
    for i in cnfg.HIDDEN_DB[table_name].find(rec_dict).sort(target_col, -1).limit(1):
        res = i

    return res


@utls.execute_query
def get_all_device_records(table_name, device_info):
    res = []
    for i in cnfg.HIDDEN_DB[table_name].find(device_info):
        res.append(i)

    return res


@utls.execute_query
def get_all_in_date(table_name, datetime_col, device_info, date_range):
    res = []
    device_info[datetime_col] = {
            "$gte": date_range['start'],
            "$lt": date_range['end']
        }
    for i in cnfg.HIDDEN_DB[table_name].find(device_info):
        res.append(i)

    return res


@utls.execute_query
def update(table_name, prim_col, info):
    res = cnfg.HIDDEN_DB[table_name].update_one(prim_col, info)
    return res.modified_count


@utls.execute_query
def update_by_filter(table_name, filter_cols, info):
    return cnfg.HIDDEN_DB[table_name].update_one(filter_cols, info)