


class InvertorSettings:

	def __init__(self):
		self.__slave_server = 'http://157.230.110.88:5000'
		self.__measureDelay = '1000'             # in milliseconds
		self.__connReistTrails = '10'


	def get_device_settings(self):
		return {
			'slave_server' : self.__slave_server,
			'measurement_delay' : self.__measureDelay,
			'conn_reist_trails' : self.__connReistTrails,
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