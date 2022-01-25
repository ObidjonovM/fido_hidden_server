from datetime import datetime
from hidden_server.models import ActionsTable
from .. import control_utils as utls


class Controller:

	def __init__(self, device_name, serial_num):
		self.__name = device_name
		self.__serial_num = serial_num
		self.__action_requested = '-'
		self.__requested_time = '-'
		self.__action_taken = '-'
		self.__action_time = '-'
		self.__actions_table = ActionsTable(device_name)


	def to_dict(self):
		return {
			'action_requested' : self.__action_requested,
			'requested_time' : self.__requested_time,
			'action_taken' : self.__action_taken,
			'action_time' : self.__action_time
		}


	def update_params(self, params):
		updated_fields = []
		
		if 'action_requested' in params:
			self.__action_requested = params['action_requested']
			updated_fields.append('action_requested')

		if 'requested_time' in params:
			self.__requested_time = params['requested_time']
			updated_fields.append('requested_time')
		
		if 'action_taken' in params:
			self.__action_taken = params['action_taken']
			updated_fields.append('action_taken')
		
		if 'action_time' in params:
			self.__action_time = params['action_time']
			updated_fields.append('action_time')
		
		return updated_fields


	def get_serial_num(self):
		return self.__serial_num


	def get_requested_action(self):
		return self.__action_requested


	def enter_new_request(self, action_requested):
		if action_requested == 'ON' or action_requested == 'OFF':
			# Update instance field values
			self.__action_requested = action_requested
			self.__action_taken = 'NO'
			now = datetime.now()
			self.__requested_time = now
			self.__action_time = now

			# Record to the db
			insert_result = self.__actions_table.insert({
					'serial_num' : self.__serial_num, 
					'action_requested' : action_requested, 
					'requested_time' : now,
					'action_taken' : 'NO',
					'action_time' : now
				})

			return {
				'success' : insert_result['success'],
				'log_code' : utls.record_log(insert_result, 'enter_new_action', 'crud_logs')
			}

		return {
			'success' : False,
			'log_code' : 0,
			'message' : 'Invalid action_requested' 
		}


	def get_last_record(self):
		result = {}
		if self.__action_requested == '-':
			get_result = self.__actions_table.get_last('log_id', {'serial_num' : self.__serial_num})
			if get_result['success'] and len(get_result['data']) > 0:
				self.__action_requested = get_result['data']['action_requested']
				self.__requested_time = get_result['data']['requested_time']
				self.__action_taken = get_result['data']['action_taken']
				self.__action_time = get_result['data']['action_time']

			result = {
				'success' : get_result['success'],
				'log_code' : utls.record_log(get_result, 'get_current_state', 'crud_logs'),
				'action_requested' : self.__action_requested,
				'requested_time' : self.__requested_time,
				'action_taken' : self.__action_taken,
				'action_time' : self.__action_time
			}

		if result == {}:
			result = {
				'success' : True,
				'log_code' : 0,        # nothing to record
				'action_requested' : self.__action_requested,
				'requested_time' : self.__requested_time,
				'action_taken' : self.__action_taken,
				'action_time' : self.__action_time			
			}

		if result['requested_time'] == 'Not ISO format':
			result['requested_time'] = '-'

		if result['action_time'] == 'Not ISO format':
			result['action_time'] = '-'

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


	def update_action(self, action_taken):
		if action_taken == 'YES' or action_taken == 'NO':

			if self.__action_requested == '-':
				get_result = self.get_last_record()	
				if self.__action_requested == '-':         # no record found in db or failure to connect to it
					return {
						'success' : get_result['success'],
						'log_code' : get_result['log_code']
					}

			action_time = datetime.now()
			update_result = self.__actions_table.update_by_filter(['serial_num', 'requested_time'], {
					'serial_num' : self.__serial_num,
					'requested_time' : self.__requested_time,
					'action_taken' : action_taken,
					'action_time' : action_time
				})

			if update_result['success']:
				self.__action_taken = action_taken
				self.__action_time = action_time
			
			return {
				'success' : update_result['success'],
				'log_code' : utls.record_log(update_result, 'update_action', 'crud_logs')
			}

		return {
			'success' : False,
			'log_code' : 0,
			'message' : 'Invalid action taken'
		}