from flask import Blueprint, request
import json
import time

from hidden_server.controls import FireSensor, Devices
from .. import views_utls as utls


fire_sensor = Blueprint('fire_sensor', __name__, url_prefix='/fire_sensor')

fire_sensors = Devices('fire_sensor')


@fire_sensor.route('/get_current_state', methods=['POST'])
def get_current_state():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_fire_sensor = FireSensor(serial_num)
	fire_sensors.load_to_device(a_fire_sensor)

	return a_fire_sensor.get_current_state()


@fire_sensor.route('/get_current_states', methods=['POST'])
def get_current_states():
	states = {}
	params = utls.get_input_params(request.data, ['serial_nums'])

	for serial_num in params['params']['serial_nums']:
		a_fire_sensor = FireSensor(serial_num)
		fire_sensors.load_to_device(a_fire_sensor)
		states[serial_num] = a_fire_sensor.get_current_state()

	return states


@fire_sensor.route('/get_all_states_in_range', methods=['POST'])
def get_all_states_in_range():
	params = utls.get_input_params(request.data, ['serial_num', 'start_date', 'end_date'])
	serial_num = params['params']['serial_num']
	a_fire_sensor = FireSensor(serial_num)
	fire_sensors.load_to_device(a_fire_sensor)

	return a_fire_sensor.get_all_states_date_range({
			'start' : utls.parse_time(params['params']['start_date']), 
			'end' : utls.parse_time(params['params']['end_date'])
		})


@fire_sensor.route('/last_request_time', methods=['POST'])
def last_request_time():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_fire_sensor = FireSensor(serial_num)
	fire_sensors.load_to_device(a_fire_sensor)

	return a_fire_sensor.get_last_request_time()


@fire_sensor.route('/from_device', methods=['POST'])
def from_device():
	params = utls.get_input_params(request.data, ['serial_num', 'state'])
	serial_num = params['params']['serial_num']
	state = params['params']['state']
	a_fire_sensor = FireSensor(serial_num)
	fire_sensors.load_to_device(a_fire_sensor)

	# Update the last request received
	update_req_res = a_fire_sensor.update_request_time()
	if not update_req_res['success']:
		return update_req_res

	# Insert state if different from the current state
	if state != a_fire_sensor.get_state():
		enter_state_res = a_fire_sensor.enter_new_state(state)
		if not enter_state_res['success']:
			return enter_state_res

	fire_sensors.add_device_params(serial_num, a_fire_sensor.to_dict())

	return update_req_res


@fire_sensor.route('/device_settings', methods=['POST'])
def device_settings():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_fire_sensor = FireSensor(serial_num)
	fire_sensors.load_to_device(a_fire_sensor)

	return a_fire_sensor.get_device_settings()