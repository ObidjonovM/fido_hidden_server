from datetime import datetime
from hidden_server.models import Measurements, DeviceSettingsTable
from .. import control_utils as utls


class TuvakMeasurements:

	MAX_SOIL_MOIST = 1044.48                # maximum soil moisture value
	TEMP_ALIGNMENT = -2                    # temperature alignment value
	SOIL_SAMPLES_LENGTH = 50              # the length of soil moisture measurement samples
	AIR_HUM_SAMPLES_LENGTH = 50           # the length of air humidity measurement samples
	TEMP_SAMPLES_LENGTH = 50              # the length of temperature measurement samples
	DECIMAL_LENGTH = 1                     # decimal length of the rounded measurement

	def __init__(self, serial_num):
		self.__name = 'tuvak'
		self.__serial_num = serial_num
		self.__soil_moist = '-'
		self.__air_humid = '-'
		self.__temp = '-'
		self.__measured_time = '-'
		self.__soil_moist_samples = []
		self.__air_samples = []
		self.__temp_samples = []
		self.__measurements_table = Measurements(self.__name)
		self.__settings_table = DeviceSettingsTable(self.__name)


	def to_dict(self):
		return {
			'soil_moist' : self.__soil_moist,
			'air_humid' : self.__air_humid,
			'temp' : self.__temp,
			'measured_time' : self.__measured_time,
			'soil_moist_samples' : self.__soil_moist_samples,
			'air_samples' : self.__air_samples,
			'temp_samples' : self.__temp_samples
		}


	def get_serial_num(self):
		return self.__serial_num


	def __get_average(self, measurements):
		if len(measurements) > 0:
			return sum(measurements) / len(measurements)

		return 0


	def __maintain_length(self):
		while len(self.__soil_moist_samples) > self.SOIL_SAMPLES_LENGTH:
			self.__soil_moist_samples.pop(0)

		while len(self.__air_samples) > self.AIR_HUM_SAMPLES_LENGTH:
			self.__air_samples.pop(0)

		while len(self.__temp_samples) > self.TEMP_SAMPLES_LENGTH:
			self.__temp_samples.pop(0)


	def update_params(self, params):
		updated_fields = []

		if 'soil_moist_samples' in params:
			self.__soil_moist_samples = params['soil_moist_samples'].copy()
			updated_fields.append('soil_moist_samples')

		if 'soil_moist' in params:
			self.__soil_moist = params['soil_moist']
			updated_fields.append('soil_moist')

		if 'air_samples' in params:
			self.__air_samples = params['air_samples'].copy()
			updated_fields.append('air_samples')

		if 'air_humid' in params:
			self.__air_humid = params['air_humid']
			updated_fields.append('air_humid')

		if 'temp_samples' in params:
			self.__temp_samples = params['temp_samples'].copy()
			updated_fields.append('temp_samples')

		if 'temp' in params:
			self.__temp = params['temp']
			updated_fields.append('temp')

		if 'measured_time' in params:
			self.__measured_time = params['measured_time']
			updated_fields.append('measured_time')

		return updated_fields


	def calibrate_params(self, params):
		updated_fields = []
		max_soil_moist = self.MAX_SOIL_MOIST
		get_result = self.__settings_table.get({'serial_num' : self.get_serial_num()})

		if len(get_result['data']) > 0:
			max_soil_moist = float(get_result['data']['max_soil_moist'])

		if 'soil_moist' in params:
			try:
				sm = ((max_soil_moist - float(params['soil_moist'])) / max_soil_moist) * 100   # aligned soil moisture value
			except ValueError:
				sm = 0

			self.__soil_moist_samples.append(sm)
			self.__soil_moist = round(self.__get_average(self.__soil_moist_samples), self.DECIMAL_LENGTH)
			updated_fields.append('soil_moist')

		if 'air_humid' in params:
			try:
				self.__air_samples.append(float(params['air_humid']))
			except ValueError:
				self.__air_samples.append(0)

			self.__air_humid = round(self.__get_average(self.__air_samples), self.DECIMAL_LENGTH)
			updated_fields.append('air_humid')

		if 'temp' in params:
			try:
				self.__temp_samples.append(float(params['temp']) + self.TEMP_ALIGNMENT)
			except:
				self.__temp_samples.append(0)
				
			self.__temp = round(self.__get_average(self.__temp_samples), self.DECIMAL_LENGTH)
			updated_fields.append('temp')

		if 'measured_time' in params:
			self.__measured_time = params['measured_time']
			updated_fields.append('measured_time')

		self.__maintain_length()

		return updated_fields


	def add_measurement(self, measurement):
		measurement['measured_time'] = datetime.now()
		self.calibrate_params(measurement)

		calibrated_params = self.to_dict()
		calibrated_params['serial_num'] = self.__serial_num
		calibrated_params.pop('soil_moist_samples')
		calibrated_params.pop('air_samples')
		calibrated_params.pop('temp_samples')
		insert_result = self.__measurements_table.insert(calibrated_params)
		
		return {
			'success' : insert_result['success'],
			'log_code' : utls.record_log(insert_result, 'insert', 'crud_logs')
		}


	def get_last_measurement(self):
		if self.__soil_moist == '-' or self.__air_humid == '-' or self.__temp == '-':
			get_result = self.__measurements_table.get_last('_id', {'serial_num' : self.__serial_num})

			if get_result['success'] and len(get_result['data']) > 0:
				self.__soil_moist = get_result['data']['soil_moist']
				self.__air_humid = get_result['data']['air_humid']
				self.__temp = get_result['data']['temp']
				self.__measured_time = get_result['data']['measured_time']

			return {
				'success' : get_result['success'],
				'log_code' : utls.record_log(get_result, 'get_last', 'crud_logs'),
				'soil_moist' : self.__soil_moist,
				'air_humid' : self.__air_humid,
				'temp' : self.__temp,
				'measured_time' : self.__measured_time
			}

		return {
			'success' : True,
			'log_code' : 0,
			'soil_moist' : self.__soil_moist,
			'air_humid' : self.__air_humid,
			'temp' : self.__temp,
			'measured_time' : self.__measured_time
		}


	def get_all_measurements_date_range(self, date_range):
		all_measurements = self.__measurements_table.get_all_date_range(
				{'serial_num' : self.__serial_num}, date_range
			)

		return {
			'success' : all_measurements['success'],
			'log_code' : utls.record_log(all_measurements, 'get_all_measurements_date_range', 'crud_logs'),
			'data' : all_measurements['data']
		}