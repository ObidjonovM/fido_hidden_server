


class WiFiLockSettings:

	def __init__(self):
		self.__slave_server = 'http://10.50.50.156:5000'
		self.__measureDelay = '1000'             # in milliseconds
		self.__min_delay = '5'
		self.__num_delays = '200'
		self.__connReistTrails = '10'


	def get_device_settings(self):
		return {
			'slave_server' : self.__slave_server,
			'measurement_delay' : self.__measureDelay,
			'min_delay' : self.__min_delay,
			'num_delays' : self.__num_delays,
			'conn_reist_trails' : self.__connReistTrails,
		}


	@property	
	def slave_server(self):
		return self.__slave_server


	@property
	def measurement_delay(self):
		return self.__measureDelay


	@property
	def min_delay(self):
		return self.__min_delay


	@property
	def num_delays(self):
		return self.__num_delays


	@property
	def conn_reist_trails(self):
		return self.__connReistTrails