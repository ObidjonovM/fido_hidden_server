from sys import exc_info
import functools


def execute_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        success = False
        data = dict()
        error_name = ''
        error_desc = ''
        error_line_num = 0
        try:
            data = func(*args, **kwargs)
            success = True

        except:
            exc_class, exc_value, exc_traceback = exc_info()
            error_name = exc_class.__name__
            error_desc = str(exc_value)
            error_line_num = exc_traceback.tb_lineno


        return {
            'success' : success,
            'data' : data,
            'error_name' : error_name,
            'error_desc' : error_desc,
            'error_line_num' : error_line_num
        }

    return wrapper