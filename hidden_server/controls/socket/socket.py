from datetime import datetime
from hidden_server.controls import Device, Controller
from hidden_server.settings import SocketSettings



class Socket():
	
	def __init__(self, serial_num):
		self.__device = Device('socket', serial_num)
		self.__control = Controller('socket', serial_num)
		self.__settings = SocketSettings()


	def to_dict(self):
		params = self.__device.to_dict()
		params.update(self.__control.to_dict())
		return params


	def update_params(self, params):
		updated_fields = self.__device.update_params(params)
		updated_fields.extend(self.__control.update_params(params))
		return updated_fields


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


	def get_requested_action(self):
		return self.__control.get_requested_action()


	def enter_new_request(self, action_requested):
		return self.__control.enter_new_request(action_requested)


	def get_last_record(self):
		return self.__control.get_last_record()


	def get_all_actions(self):
		return self.__control.get_all_actions()


	def get_all_actions_date_range(self, date_range):
		return self.__control.get_all_actions_date_range(date_range)


	def update_action(self, action_taken):
		return self.__control.update_action(action_taken)


	def get_device_settings(self):
		device_settings = self.__device.get_device_settings()
		if device_settings['success'] and len(device_settings['settings']) > 0:
			return device_settings['settings']

		return self.__settings.get_device_settings()