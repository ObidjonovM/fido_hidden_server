import logging
import os
import sys
from datetime import datetime
from hidden_server import config
from hidden_server.models import ErrorLogsTable


def get_logger(name, log_file):
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(message)s')
    handler = logging.FileHandler(os.path.join(config.LOGS_PATH, log_file))
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    return logger
     

def record_log(result, func_name, logger_name):
    if result['success']:
        return 0       # no need to record

    log_result = ErrorLogsTable.insert_log({
        'serial_num' : result['serial_num'],
        'call_path' : os.path.abspath(__file__),
        'function_name' : func_name,
        'line_number' : result['error_line_num'],
        'error_name' : result['error_name'],
        'description' : result['error_desc'],
        'date_added' : datetime.now()
    })

    if log_result['success']:
        if result['error_name'] == 'UniqueViolation':
            return -1          # recorded to error logs table
        
        return -2         # recorded to error logs table

    try:
        logger = get_logger(logger_name, f'{logger_name}.log')
        logger.error(log_result['error_desc'])
        return -3             # recorded to logs file

    except:
        print('Error could not be logged')
        t, v, _ = sys.exc_info()
        print(f'{t} - {v}')

    return -4       # could not record logs anywhere