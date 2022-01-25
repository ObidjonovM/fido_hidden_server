from datetime import datetime
from hidden_server.controls import Device
from hidden_server.settings import WaterSensorSettings




class WaterSensor:
	def __init__(self, serial_num):
		self.__device = Device('water_sensor', serial_num)
		self.__settings = WaterSensorSettings()


	def to_dict(self):
		return self.__device.to_dict()


	def update_params(self, params):
		return self.__device.update_params(params)


	def get_serial_num(self):
		return self.__device.get_serial_num()


	def get_state(self):
		return self.__device.get_state()


	def enter_new_state(self, new_state):
		return self.__device.enter_new_state(new_state)


	def get_current_state(self):
		return self.__device.get_current_state()


	def get_all_states(self):
		return self.__device.get_all_states()


	def get_all_states_date_range(self, date_range):
		return self.__device.get_all_states_date_range(date_range)


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