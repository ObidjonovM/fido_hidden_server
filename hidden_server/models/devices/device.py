from .. import crud


class DeviceStateTable:

	def __init__(self, name):
		self.name = name + '_state'


	def insert(self, state_info):
		result = crud.insert(self.name, state_info)
		result['serial_num'] = state_info['serial_num']
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
		result = crud.get_all_in_date(self.name, 'state_time', device_info, date_range)
		result['serial_num'] = device_info['serial_num']
		return result


	def update(self, prim_col, state_info):
		pass


	def delete(self, state_info):
		pass


class DeviceRequestTimesTable:

	def __init__(self, name):
		self.name = name + '_request_times'


	def insert(self, req_info):
		result = crud.insert(self.name, req_info, False)
		result['serial_num'] = req_info['serial_num']
		return result


	def get(self, req_info):
		result = crud.get(self.name, req_info)
		result['serial_num'] = req_info['serial_num']
		return result


	def update(self, prim_col, req_info):
		result = crud.update(self.name, prim_col, req_info)
		result['serial_num'] = req_info['serial_num']
		return result


	def delete(self, req_info):
		pass


class DeviceSettingsTable:
	def __init__(self, name):
		self.name = name + '_settings'


	def insert(self, settings_info):
		result = crud.insert(self.name, device_info, False)
		result['serial_num'] = settings_info['serial_num']
		return result


	def get(self, req_info):
		result = crud.get(self.name, req_info)

		# converting settings values to strings to validate with ESP devices
		if len(result.get('data')) > 0:
			for k in result['data'].keys():
				result['data'][k] = str(result['data'][k])

		result['serial_num'] = req_info['serial_num']
		return result


	def update(self, prim_col, settings_info):
		result = crud.update(self.name, prim_col, settings_info)
		result['serial_num'] = settings_info['serial_num']
		return result


	def delete(self, req_info):
		pass


class GetGasValueTable:
	def __init__(self, name):
		self.name = name + '_values'


	def insert(self, val_info):
		result = crud.insert(self.name, val_info)
		result['serial_num'] = val_info['serial_num']
		return result


	def get_last(self, target_col, rec_info):
		result = crud.get_last(self.name, target_col, rec_info)
		result['serial_num'] = rec_info['serial_num']
		return result


	def get_all_date_range(self, device_info, date_range):
		result = crud.get_all_in_date(self.name, 'gas_value_time', device_info, date_range)
		result['serial_num'] = device_info['serial_num']
		return result


	def update(self, prim_col, settings_info):
		result = crud.update(self.name, prim_col, settings_info)
		result['serial_num'] = settings_info['serial_num']
		return result


	def delete(self, req_info):
		pass