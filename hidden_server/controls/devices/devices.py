import redis
from datetime import datetime
from decimal import Decimal
import json
import pickle

class Devices:

	def __init__(self, name):
		self.__name = name
		self.__devices = redis.Redis()


	def __to_redis_format(self, params):
		rf_params = {}

		for k,v in params.items():
			if isinstance(v, datetime):
				rf_params[k] = v.isoformat()
			elif isinstance(v, list):
				rf_params[k] = str(v)
			elif isinstance(v, Decimal):
				rf_params[k] = str(v)
			else:
				rf_params[k] = v

		return rf_params


	def __str2list(self, strlist):                  # converts list in string representation to list
		try:
			return [float(num) for num in strlist[1:-1].split(',')]

		except:
			return []


	def __from_redis_format(self, rf_params):
		if rf_params == {}:
			return {}

		params = {}
		for k,v in rf_params.items():
			ks = k.decode('utf-8')
			vs = v.decode('utf-8')
			if vs != "-":
				if ks.endswith('_time'):
					try:
						params[ks] = datetime.fromisoformat(vs)
					except ValueError:
						params[ks] = 'Not ISO format'
				elif ks.endswith('_samples'):
					params[ks] = self.__str2list(vs)
				else:
					params[ks] = vs
			else:
				params[ks] = vs

		return params


	
	def add_device_params(self, serial_num, device_params):
		params = self.__to_redis_format(device_params)
		result = self.__devices.hmset(
				serial_num, 
				params)

		return result


	def load_to_device(self, device):
		serial_num = device.get_serial_num()
		params = self.__devices.hgetall(serial_num)
		params = self.__from_redis_format(params)
		if params != {}:
			device.update_params(params)



	# def remove_device(self, serial_num):
	# 	self.__devices.del(serial_num)

