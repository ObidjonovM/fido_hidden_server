from datetime import datetime
from hidden_server.controls import Device, GetGasValue
from hidden_server.settings import GasSensorSettings



class GasSensor:
	
	def __init__(self, serial_num):
		self.__device = Device('gas_sensor', serial_num)
		self.__enter_gas_value = GetGasValue('gas_sensor', serial_num)
		self.__settings = GasSensorSettings()


	def to_dict(self):
		params = self.__device.to_dict()
		params.update(self.__enter_gas_value.to_dict())
		return params


	def update_params(self, params):
		updated_fields = self.__device.update_params(params)
		updated_fields.extend(self.__enter_gas_value.update_params(params))
		return updated_fields


	def get_serial_num(self):
		return self.__device.get_serial_num()


	def get_gas_value(self):
		return self.__enter_gas_value.get_gas_value()


	def get_state(self):
		return self.__device.get_state()


	def enter_new_state(self, new_state):
		return self.__device.enter_new_state(new_state)


	def enter_gas_value(self, new_value):
		gv = self.get_gas_value()
		curr_gas_val = float(gv) if gv != '-' else 0.00
		var_value = self.__settings.var_value
		if not curr_gas_val - var_value <= new_value <= curr_gas_val + var_value:
			return self.__enter_gas_value.enter_gas_value(new_value)

		return {
			'success' : True,
			'log_code' : 0
		}


	def get_current_value(self):
		return self.__enter_gas_value.get_current_value()


	def get_current_state(self):
		return self.__device.get_current_state()


	def get_all_states(self):
		return self.__device.get_all_states()


	def get_all_states_date_range(self, date_range):
		return self.__device.get_all_states_date_range(date_range)


	def get_all_values_date_range(self, date_range):
		return self.__enter_gas_value.get_all_values_date_range(date_range)


	def add_device_request_time(self):
		return self.__device.add_device_request_time()


	def get_last_request_time(self):
		return self.__device.get_last_request_time()


	def update_request_time(self):
		return self.__device.update_request_time()


	def get_device_settings(self):
		device_settings = self.__device.get_device_settings()
		if device_settings['success'] and len(device_settings['settings']) > 0:
			return device_settings['settings']

		return self.__settings.get_device_settings()