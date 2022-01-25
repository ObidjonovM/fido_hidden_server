from flask import Blueprint, request
import json
import time

from hidden_server.controls import VibrationSensor, Devices
from .. import views_utls as utls


vibration_sensor = Blueprint('vibration_sensor', __name__, url_prefix='/vibration_sensor')

vibration_sensors = Devices('vibration_sensor')


@vibration_sensor.route('/get_current_state', methods=['POST'])
def get_current_state():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_vibration_sensor = VibrationSensor(serial_num)
	vibration_sensors.load_to_device(a_vibration_sensor)
	
	return a_vibration_sensor.get_current_state()


@vibration_sensor.route('/get_current_states', methods=['POST'])
def get_current_states():
	states = {}
	params = utls.get_input_params(request.data, ['serial_nums'])
	for serial_num in params['params']['serial_nums']:
		a_vibration_sensor = VibrationSensor(serial_num)
		vibration_sensors.load_to_device(a_vibration_sensor)
		states[serial_num] = a_vibration_sensor.get_current_state()

	return states


@vibration_sensor.route('/get_all_states_in_range', methods=['POST'])
def get_all_states_in_range():
	params = utls.get_input_params(request.data, ['serial_num', 'start_date', 'end_date'])
	serial_num = params['params']['serial_num']
	a_vibration_sensor = VibrationSensor(serial_num)
	vibration_sensors.load_to_device(a_vibration_sensor)

	return a_vibration_sensor.get_all_states_date_range({
			'start' : utls.parse_time(params['params']['start_date']), 
			'end' : utls.parse_time(params['params']['end_date'])
		})


@vibration_sensor.route('/last_request_time', methods=['POST'])
def last_request_time():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_vibration_sensor = VibrationSensor(serial_num)
	vibration_sensors.load_to_device(a_vibration_sensor)

	return a_vibration_sensor.get_last_request_time()


@vibration_sensor.route('/from_device', methods=['POST'])
def from_device():
	params = utls.get_input_params(request.data, ['serial_num', 'state'])

	serial_num = params['params']['serial_num']
	state = params['params']['state']
	a_vibration_sensor = VibrationSensor(serial_num)
	vibration_sensors.load_to_device(a_vibration_sensor)

	# Update the last request received
	update_req_res = a_vibration_sensor.update_request_time()
	if not update_req_res['success']:
		return update_req_res

	# Insert state if different from the current state
	if state != a_vibration_sensor.get_state():
		enter_state_res = a_vibration_sensor.enter_new_state(state)
		if not enter_state_res['success']:
			return enter_state_res

	return update_req_res


@vibration_sensor.route('/device_settings', methods=['POST'])
def device_settings():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_vibration_sensor = VibrationSensor(serial_num)
	vibration_sensors.load_to_device(a_vibration_sensor)

	return a_vibration_sensor.get_device_settings()