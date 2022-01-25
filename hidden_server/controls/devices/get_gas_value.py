from datetime import datetime
from hidden_server.models import GetGasValueTable
from .. import control_utils as utls


class GetGasValue:

    def __init__(self, device_name, serial_num):
        self.__serial_num = serial_num
        self.__gas_value = '-'
        self.__gas_value_time = '-'
        self.__gas_value_table = GetGasValueTable(device_name)


    def to_dict(self):
        return {
            'gas_value' : self.__gas_value,
            'gas_value_time' : self.__gas_value_time
        }


    def update_params(self, params):
        update_fields = []

        if 'gas_value' in params:
            self.__gas_value = params['gas_value']
            update_fields.append('gas_value')

        if 'gas_value_time' in params:
            self.__gas_value_time = params['gas_value_time']
            update_fields.append('gas_value_time')

        return update_fields


    def get_gas_value(self):
        if self.__gas_value == '-':
            self.get_current_value()

        return self.__gas_value


    def enter_gas_value(self, new_value):

        value_change_time = datetime.now()

        self.__gas_value = new_value
        self.__gas_value_time = value_change_time

        insert_result = self.__gas_value_table.insert({
				'serial_num' : self.__serial_num,
				'gas_value' : new_value,
				'gas_value_time' : value_change_time
			})

        return {
			'success' : insert_result['success'],
			'log_code' : utls.record_log(insert_result, 'insert', 'crud_logs')
		}


    def get_current_value(self):
        if self.__gas_value == '-' or self.__gas_value_time == '-':
            get_result = self.__gas_value_table.get_last('log_id', {
					'serial_num' : self.__serial_num
				})

            if get_result['success'] and len(get_result['data']) > 0:
                self.__gas_value = str(get_result['data']['gas_value'])
                self.__gas_value_time = get_result['data']['gas_value_time']

            return {
				'success' : get_result['success'],
				'log_code' : utls.record_log(get_result, 'get_last', 'crud_logs'),
				'gas_value' : self.__gas_value,
				'gas_value_time' : self.__gas_value_time
			}

        return {
			'success' : True,
			'log_code' : 0,         # no need to record
			'gas_value' : self.__gas_value,
			'gas_value_time' : self.__gas_value_time
		}


    def get_all_values_date_range(self, date_range):
        all_states_dr_result = self.__gas_value_table.get_all_date_range(
				{'serial_num' : self.__serial_num}, date_range
			)

        return {
			'success' : all_states_dr_result['success'],
			'log_code' : utls.record_log(all_states_dr_result, 'get_all_states_date_range', 'crud_logs'),
			'data' : all_states_dr_result['data']
		}