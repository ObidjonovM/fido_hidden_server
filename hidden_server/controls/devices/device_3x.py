from datetime import datetime
from hidden_server.models import DeviceStateTable, DeviceRequestTimesTable, DeviceSettingsTable
from .. import control_utils as utls


class Device3x:

	def __init__(self, device_name, serial_num):
		self.__serial_num = serial_num
		self.__states = {'left' : '-', 'center' : '-', 'right' : '-'}
		self.__state_change_time = '-'
		self.__last_request_time = '-'
		self.__state_table = DeviceStateTable(device_name)
		self.__request_times_table = DeviceRequestTimesTable(device_name)
		self.__settings_table = DeviceSettingsTable(device_name)


	def to_dict(self):
		return {
			'state_left' : self.__states['left'],
			'state_center' : self.__states['center'],
			'state_right' : self.__states['right'],
			'state_time' : self.__state_change_time,
			'last_request_time' : self.__last_request_time
		}


	def update_params(self, params):
		updated_fields = []

		for k in self.__states.keys():
			field = 'state_' + k
			if field in params:
				self.__states[k] = params[field]
				updated_fields.append(field)

		if 'state_change_time' in params:
			self.__state_change_time = params['state_change_time']
			updated_fields.append('state_change_time')
		
		if 'last_request_time' in params:
			self.__last_request_time = params['last_request_time']
			updated_fields.append('last_request_time')
		
		return updated_fields
		

	def get_serial_num(self):
		return self.__serial_num


	def __no_record(self):
		for v in self.to_dict().values():
			if v == '-':
				return True

		return False


	def get_states(self):
		if self.__no_record():
			self.get_current_states()

		return self.__states


	def __valid_states(self, states):
		for k, v in states.items():
			if not (k in ['left', 'center', 'right'] and
				v in ['ON', 'OFF']):
				return False

		return True


	def enter_new_states(self, new_states):
		#Check for input validity
		if not self.__valid_states(new_states):
			return {
				'success' : False,
				'log_code' : -5
			}

		state_change_time = datetime.now()

		# Update the current state and state_change_time
		self.__states.update(new_states)
		self.__state_change_time = state_change_time

		# Enter the new_state and and current timestamp into the "*_state" table
		insert_result = self.__state_table.insert({
				'state_time' : state_change_time, 
				'serial_num' : self.__serial_num, 
				'state_left' : new_states['left'],
				'state_center' : new_states['center'],
				'state_right' : new_states['right']
			})

		return {
			'success' : insert_result['success'],
			'log_code' : utls.record_log(insert_result, 'insert', 'crud_logs')
		}


	def get_current_states(self):
		if self.__no_record():
			get_result = self.__state_table.get_last('log_id', {
					'serial_num' : self.__serial_num
				})

			if get_result['success'] and len(get_result['data']) > 0:
				self.__states['left'] = get_result['data']['state_left']
				self.__states['center'] = get_result['data']['state_center']
				self.__states['right'] = get_result['data']['state_right']
				self.__state_change_time = get_result['data']['state_time']

			return {
				'success' : get_result['success'],
				'log_code' : utls.record_log(get_result, 'get_last', 'crud_logs'),
				'state_change_time' : self.__state_change_time,
				'state_left' : self.__states['left'],
				'state_center' : self.__states['center'],
				'state_right' : self.__states['right']
			}

		return {
			'success' : True,
			'log_code' : 0,         # no need to record
			'state_left' : self.__states['left'],
			'state_center' : self.__states['center'],
			'state_right' : self.__states['right'],
			'state_change_time' : self.__state_change_time,
		}


	def get_all_states(self):
		all_states_result = self.__state_table.get_all({
				'serial_num' : self.__serial_num
			})

		return {
			'success' : all_states_result['success'],
			'log_code' : utls.record_log(all_states_result, 'get_all_states', 'crud_logs'),
			'data' : all_states_result['data']
		}


	def get_all_states_date_range(self, date_range):
		all_states_dr_result = self.__state_table.get_all_date_range(
				{'serial_num' : self.__serial_num}, date_range
			)

		return {
			'success' : all_states_dr_result['success'],
			'log_code' : utls.record_log(all_states_dr_result, 'get_all_states_date_range', 'crud_logs'),
			'data' : all_states_dr_result['data']
		}


	def add_device_request_time(self):
		add_device_result = self.__request_times_table.insert({
				'serial_num' : self.__serial_num,
				'request_time' : datetime.now()
			})

		return {
			'success' : add_device_result['success'],
			'log_code' : utls.record_log(add_device_result, 'add_device_request_time', 'crud_logs')
		}


	def get_last_request_time(self):
		if self.__last_request_time == '-':
			get_req_time_result = self.__request_times_table.get({
					'serial_num' : self.__serial_num
				})

			if get_req_time_result['success'] and len(get_req_time_result['data']) > 0:
				self.__last_request_time = get_req_time_result['data']['request_time']
			
			return {
				'success' : get_req_time_result['success'],
				'log_code' : utls.record_log(get_req_time_result, 'get_last_request_time', 'crud_logs'),
				'request_time' : self.__last_request_time
			}

		return {
			'success' : True,
			'log_code' : 0,    # no need to record
			'request_time' : self.__last_request_time
		}


	def update_request_time(self):
		if self.__last_request_time == '-':
			last_request_db = self.get_last_request_time()

			if not last_request_db['success']:
				return {
					'success' : last_request_db['success'],
					'log_code' : last_request_db['log_code']
				}

			if last_request_db['request_time'] == '-':     # the device is not in the db yet
				add_result = self.add_device_request_time()     # add the device to the db

				if not add_result['success']:                    # could not add the device to the db
					return {
						'success' : add_result['success'],
						'log_code' : add_result['log_code']
					}

		# successfully added if was not in the db, now we can synchronize instance and db values
		request_time = datetime.now()
		self.__last_request_time = request_time
		update_result = self.__request_times_table.update('serial_num', {
				'serial_num' : self.__serial_num,
				'request_time' : request_time
			})
		
		return {
			'success' : update_result['success'],
			'log_code' : utls.record_log(update_result, 'update_request_time', 'crud_logs')
		}


	def get_device_settings(self):
		get_result = self.__settings_table.get({'serial_num' : self.get_serial_num()})

		return {
			'success' : get_result['success'],
			'log_code' : utls.record_log(get_result, 'get_last', 'crud_logs'),
			'settings' : get_result['data']
		}