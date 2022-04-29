


class FireSensorSettings:

	def __init__(self):
		self.__slave_server = 'http://10.50.50.156:5000'
		self.__measureDelay = '1000'             # in milliseconds
		self.__connReistTrails = '10'
		self.__maxGasVal = '100'
		self.__buzzDuration = '200'
		self.__buzzInterval = '500'


	def get_device_settings(self):
		return {
			'slave_server' : self.__slave_server,
			'measurement_delay' : self.__measureDelay,
			'conn_reist_trails' : self.__connReistTrails,
			'max_gas_value' : self.__maxGasVal,
			'buzz_duration' : self.__buzzDuration,
			'buzz_interval' : self.__buzzInterval
		}


	@property	
	def slave_server(self):
		return self.__slave_server


	@property
	def measurement_delay(self):
		return self.__measureDelay


	@property
	def conn_reist_trails(self):
		return self.__connReistTrails


	@property
	def max_gas_value(self):
		return self.__maxGasVal


	@property
	def buzz_duration(self):
		return self.__buzzDuration


	@property
	def buzz_interval(self):
		return self.__buzzInterval