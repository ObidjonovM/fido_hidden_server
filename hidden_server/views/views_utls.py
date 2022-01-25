import json
from datetime import datetime


def get_input_params(raw_data, expected_params_list):
	try:
		params = json.loads(raw_data)
		for param in params:
			if not param in expected_params_list:
				raise KeyError

	except json.JSONDecodeError:
		return {
			'status_code' : -1,
			'status' : 'Not a JSON format'
		}

	except KeyError:
		return {
			'status_code' : -2,
			'status' : 'Input error. Invalid field name'
		}

	except:
		return {
			'status_code' : -3,
			'status' : 'Unknown error'
		}

	return {
		'status_code' : 0,
		'status' : 'OK',
		'params' : params
	}


def get_input_params_all(raw_data):
	try:
		params = json.loads(raw_data)

	except json.JSONDecodeError:
		return {
			'status_code' : -1,
			'status' : 'Not a JSON format'
		}

	except:
		return {
			'status_code' : -3,
			'status' : 'Unknown error'
		}

	return {
		'status_code' : 0,
		'status' : 'OK',
		'params' : params
	}


def parse_time(str_time):
	return datetime.strptime(str_time, '%Y-%m-%dT%H:%M')
