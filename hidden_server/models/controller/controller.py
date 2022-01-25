from .. import crud



class ActionsTable:

	def __init__(self, name):
		self.name = name + '_actions'


	def insert(self, action_info):
		result = crud.insert(self.name, action_info)
		result['serial_num'] = action_info['serial_num']
		return result


	def get_last(self, target_col, device_info):
		result = crud.get_last(self.name, target_col, device_info)
		result['serial_num'] = device_info['serial_num']
		return result


	def get_all(self, device_info):
		result = crud.get_all_device_records(self.name, device_info)
		result['serial_num'] = device_info['serial_num']
		return result


	def get_all_date_range(self, device_info, date_range):
		result = crud.get_all_in_date(self.name, 'requested_time', device_info, date_range)
		result['serial_num'] = device_info['serial_num']
		return result


	def update_by_filter(self, filter_cols, action_info):
		result = crud.update_by_filter(self.name, filter_cols, action_info)
		result['serial_num'] = action_info['serial_num']
		return result