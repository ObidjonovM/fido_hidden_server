from flask import Blueprint, request
import json
import time

from hidden_server.controls import WaterSensor, Devices
from .. import views_utls as utls


water_sensor = Blueprint('water_sensor', __name__, url_prefix='/water_sensor')

water_sensors = Devices('water_sensor')


@water_sensor.route('/get_current_state', methods=['POST'])
def get_current_state():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_water_sensor = WaterSensor(serial_num)
	water_sensors.load_to_device(a_water_sensor)
	
	return a_water_sensor.get_current_state()


@water_sensor.route('/get_current_states', methods=['POST'])
def get_current_states():
	states = {}
	params = utls.get_input_params(request.data, ['serial_nums'])
	for serial_num in params['params']['serial_nums']:
		a_water_sensor = WaterSensor(serial_num)
		water_sensors.load_to_device(a_water_sensor)
		states[serial_num] = a_water_sensor.get_current_state()

	return states


@water_sensor.route('/get_all_states_in_range', methods=['POST'])
def get_all_states_in_range():
	params = utls.get_input_params(request.data, ['serial_num', 'start_date', 'end_date'])
	serial_num = params['params']['serial_num']
	a_water_sensor = WaterSensor(serial_num)
	water_sensors.load_to_device(a_water_sensor)

	return a_water_sensor.get_all_states_date_range({
			'start' : utls.parse_time(params['params']['start_date']), 
			'end' : utls.parse_time(params['params']['end_date'])
		})


@water_sensor.route('/last_request_time', methods=['POST'])
def last_request_time():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_water_sensor = WaterSensor(serial_num)
	water_sensors.load_to_device(a_water_sensor)
	
	return a_water_sensor.get_last_request_time()


@water_sensor.route('/from_device', methods=['POST'])
def from_device():
	params = utls.get_input_params(request.data, ['serial_num', 'state'])
	serial_num = params['params']['serial_num']
	state = params['params']['state']
	a_water_sensor = WaterSensor(serial_num)
	water_sensors.load_to_device(a_water_sensor)

	# Update the last request received
	update_req_res = a_water_sensor.update_request_time()
	if not update_req_res['success']:
		return update_req_res

	# Insert state if different from the current state
	if state != a_water_sensor.get_state():
		enter_state_res = a_water_sensor.enter_new_state(state)
		if not enter_state_res['success']:
			return enter_state_res

	return update_req_res


@water_sensor.route('/device_settings', methods=['POST'])
def device_settings():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_water_sensor = WaterSensor(serial_num)
	water_sensors.load_to_device(a_water_sensor)

	return a_water_sensor.get_device_settings()