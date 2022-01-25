from .. import crud


class Measurements:

	def __init__(self, name):
		self.name = name + '_measurements'


	def insert(self, measurements):
		result = crud.insert(self.name, measurements)
		result['serial_num'] = measurements['serial_num']
		return result


	def get_last(self, target_col, rec_info):
		result = crud.get_last(self.name, target_col, rec_info)
		result['serial_num'] = rec_info['serial_num']
		return result


	def get_all(self, device_info):
		result = crud.get_all_device_records(self.name, device_info)
		result['serial_num'] = device_info['serial_num']
		return result


	def get_all_date_range(self, device_info, date_range):
		result = crud.get_all_in_date(self.name, 'measured_time', device_info, date_range)
		result['serial_num'] = device_info['serial_num']
		return result


	def update(self, prim_col, state_info):
		pass


	def delete(self, state_info):
		pass