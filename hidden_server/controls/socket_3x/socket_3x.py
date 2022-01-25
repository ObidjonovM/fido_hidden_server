from datetime import datetime
from hidden_server.controls import Device3x, Controller3x
from hidden_server.settings import Socket3xSettings



class Socket3x:
	def __init__(self, serial_num):
		self.__device = Device3x('socket_3x', serial_num)
		self.__control = Controller3x('socket_3x', serial_num)
		self.__settings = Socket3xSettings()


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


	def get_states(self):
		return self.__device.get_states()


	def enter_new_states(self, new_state):
		return self.__device.enter_new_states(new_state)


	def get_current_state(self):
		return self.__device.get_current_states()


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
		return self.__control.get_requested_actions()


	def enter_new_request(self, action_requested):
		return self.__control.enter_new_request(action_requested)


	def get_last_record(self):
		return self.__control.get_last_record()


	def get_all_actions(self):
		return self.__control.get_all_actions()


	def get_all_actions_date_range(self, date_range):
		return self.__control.get_all_actions_date_range(date_range)


	def update_actions(self, actions_taken):
		return self.__control.update_actions(actions_taken)


	def get_device_settings(self):
		device_settings = self.__device.get_device_settings()
		if device_settings['success'] and len(device_settings['settings']) > 0:
			return device_settings['settings']

		return self.__settings.get_device_settings()