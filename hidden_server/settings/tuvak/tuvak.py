


class TuvakSettings:

	def __init__(self):
		self.__slave_server = 'http://10.50.50.156:5000'
		self.__measurement_delay = '1000'             # in milliseconds
		self.__pump_on_delay = '10000'
		self.__moist_samples = '50'
		self.__conn_reist_trails = '10'

		# Tuvak unique constants
		self.__record_interval = 60 * 5            # 5 minutes


	def get_device_settings(self):
		return {
			'slave_server' : self.__slave_server,
			'measurement_delay' : self.__measurement_delay,
			'pump_on_delay' : self.__pump_on_delay,
			'moist_samples' : self.__moist_samples,
			'conn_reist_trails' : self.__conn_reist_trails,
		}


	@property	
	def slave_server(self):
		return self.__slave_server


	@property
	def measurement_delay(self):
		return self.__measurement_delay


	@property
	def conn_reist_trails(self):
		return self.__conn_reist_trails


	@property
	def pump_on_delay(self):
		return self.__pump_on_delay


	@property
	def moist_samples(self):
		return self.__moist_samples


	@property
	def record_interval(self):
		return self.__record_interval
	