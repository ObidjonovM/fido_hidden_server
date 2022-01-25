from .. import crud

class ErrorLogsTable:


    @staticmethod
    def insert_log(log_info):
        return crud.insert('error_logs', log_info)


    @staticmethod
    def get_log_info(log_id):
        pass


    @staticmethod
    def get_log_info_all():
        return crud.get_all('error_logs')


    @staticmethod
    def update_log_info(log_info):
        pass


    @staticmethod
    def delete_log(log_id):
        pass