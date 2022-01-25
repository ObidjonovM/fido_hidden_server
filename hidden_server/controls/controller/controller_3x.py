from datetime import datetime
from hidden_server.models import ActionsTable
from .. import control_utils as utls


class Controller3x:

	def __init__(self, device_name, serial_num):
		self.__name = device_name
		self.__serial_num = serial_num
		self.__requested_time = '-'
		self.__actions_requested = {'left' : '-', 'center' : '-', 'right' : '-'}
		self.__requested_times = {'left' : '-', 'center' : '-', 'right' : '-'}
		self.__actions_taken = {'left' : '-', 'center' : '-', 'right' : '-'}
		self.__action_times = {'left' : '-', 'center' : '-', 'right' : '-'}
		self.__actions_table = ActionsTable(device_name)


	def to_dict(self):
		return {
			'requested_time' : self.__requested_time,
			'action_requested_left' : self.__actions_requested['left'],
			'action_requested_center' : self.__actions_requested['center'],
			'action_requested_right' : self.__actions_requested['right'],
			'requested_time_left' : self.__requested_times['left'],
			'requested_time_center' : self.__requested_times['center'],
			'requested_time_right' : self.__requested_times['right'],
			'action_taken_left' : self.__actions_taken['left'],
			'action_taken_center' : self.__actions_taken['center'],
			'action_taken_right' : self.__actions_taken['right'],
			'action_time_left' : self.__action_times['left'],
			'action_time_center' : self.__action_times['center'],
			'action_time_right' : self.__action_times['right']
		}


	def update_params(self, params):
		updated_fields = []

		if 'requested_time' in params:
			self.__requested_time = params['requested_time']
			updated_fields.append('requested_time')

		for k in ['left', 'center', 'right']:
			action_requested = 'action_requested_' + k
			if action_requested in params:
				self.__actions_requested[k] = params[action_requested]
				updated_fields.append(action_requested)

			requested_time = 'requested_time_' + k
			if requested_time in params:
				self.__requested_times[k] = params[requested_time]
				updated_fields.append(requested_time)

			action_taken = 'action_taken_' + k
			if action_taken in params:
				self.__actions_taken[k] = params[action_taken]
				updated_fields.append(action_taken)

			action_time = 'action_time_' + k
			if action_time in params:
				self.__action_times[k] = params[action_time]
				updated_fields.append(action_time)
				
		return updated_fields


	def get_serial_num(self):
		return self.__serial_num


	def get_requested_actions(self):
		return self.__actions_requested 


	def __valid_requests(self, actions_requested):
		valid_fields = ['action_requested_left','action_requested_center','action_requested_right']
		for k, v in actions_requested.items():
			if not k in valid_fields:
				return False

			if not v in ['ON', 'OFF']:
				return False

		return True
				

	def enter_new_request(self, actions_requested):
		if self.__valid_requests(actions_requested):
			now = datetime.now()
			self.__requested_time = now
			for k, v in actions_requested.items():
				side = k.split('_')[-1]
				self.__actions_requested[side] = v
				self.__requested_times[side] = now
				self.__actions_taken[side] = 'NO'
				self.__action_times[side] = now

			# Record to the db
			data = self.to_dict()
			data.update({'serial_num' : self.__serial_num})
			insert_result = self.__actions_table.insert(data)

			return {
				'success' : insert_result['success'],
				'log_code' : utls.record_log(insert_result, 'enter_new_action', 'crud_logs')
			}

		return {
			'success' : False,
			'log_code' : 0,
			'message' : 'Invalid action_requested' 
		}


	def __no_record(self):
		for v in self.to_dict().values():
			if v == '-':
				return True

		return False


	def get_last_record(self):
		success = True
		log_code = 0

		if self.__no_record():
			get_result = self.__actions_table.get_last('log_id', {'serial_num' : self.__serial_num})
			success = get_result['success']
			log_code = utls.record_log(get_result, 'get_current_state', 'crud_logs')

			if success and len(get_result['data']) > 0:
				self.update_params(get_result['data'])

		result = {'success' : success, 'log_code' : log_code}
		result.update(self.to_dict())

		return result


	def get_all_actions(self):
		all_actions_result = self.__actions_table.get_all({'serial_num' : self.__serial_num})
		
		return {
			'success' : all_actions_result['success'],
			'log_code' : utls.record_log(all_actions_result, 'get_all_actions', 'crud_logs'),
			'data' : all_actions_result['data']
		}


	def get_all_actions_date_range(self, date_range):
		all_actions_dr_result = self.__actions_table.get_all_date_range(
				{'serial_num' : self.__serial_num}, date_range
			)

		return {
			'success' : all_actions_dr_result['success'],
			'log_code' : utls.record_log(all_actions_dr_result, 'get_all_actions_date_range', 'crud_logs'),
			'data' : all_actions_dr_result['data']
		}


	def __valid_actions(self, actions_taken):
		valid_actions = ['action_taken_left', 'action_taken_center', 'action_taken_right']
		for k, v in actions_taken.items():
			if not k in valid_actions:
				return False

			if not v in ['YES', 'NO']:
				return False

		return True


	def update_actions(self, actions_taken):
		if self.__valid_actions(actions_taken):
			if self.__no_record():
				get_result = self.get_last_record()	
				if self.__no_record():					# no record found in db or failure to connect to it
					return {
						'success' : get_result['success'],
						'log_code' : get_result['log_code']
					}

			# prepare data for updating
			action_time = datetime.now()
			filters = ['serial_num']
			data = {'serial_num' : self.__serial_num}
			for k, v in actions_taken.items():
				side = k.split('_')[-1]
				req_time = 'requested_time_' + side
				filters.append(req_time)
				data[req_time] = self.__requested_times[side]
				data[k] = v
				data['action_time_' + side] = action_time

			update_result = self.__actions_table.update_by_filter(filters, data)
			if update_result['success']:
				for k, v in actions_taken.items():
					side = k.split('_')[-1]
					self.__actions_taken[side] = v
					self.__action_times[side] = action_time
			
			return {
				'success' : update_result['success'],
				'log_code' : utls.record_log(update_result, 'update_actions', 'crud_logs')
			}

		return {
			'success' : False,
			'log_code' : 0,
			'message' : 'Invalid action taken'
		}