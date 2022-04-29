from flask import Blueprint, request
import json
import time

from hidden_server.controls import GasSensor, Devices
from .. import views_utls as utls


gas_sensor = Blueprint('gas_sensor', __name__, url_prefix='/gas_sensor')

gas_sensors = Devices('gas_sensor')


@gas_sensor.route('/get_current_state', methods=['POST'])
def get_current_state():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_gas_sensor = GasSensor(serial_num)
	gas_sensors.load_to_device(a_gas_sensor)

	return a_gas_sensor.get_current_state()


@gas_sensor.route('/get_current_states', methods=['POST'])
def get_current_states():
	states = {}
	params = utls.get_input_params(request.data, ['serial_nums'])

	for serial_num in params['params']['serial_nums']:
		a_gas_sensor = GasSensor(serial_num)
		gas_sensors.load_to_device(a_gas_sensor)
		states[serial_num] = a_gas_sensor.get_current_state()

	return states


@gas_sensor.route('/get_all_states_in_range', methods=['POST'])
def get_all_states_in_range():
	params = utls.get_input_params(request.data, ['serial_num', 'start_date', 'end_date'])
	serial_num = params['params']['serial_num']
	a_gas_sensor = GasSensor(serial_num)
	gas_sensors.load_to_device(a_gas_sensor)

	return a_gas_sensor.get_all_states_date_range({
			'start' : utls.parse_time(params['params']['start_date']), 
			'end' : utls.parse_time(params['params']['end_date'])
		})


@gas_sensor.route('/get_all_values_in_range', methods=['POST'])
def get_all_values_in_range():
	params = utls.get_input_params(request.data, ['serial_num', 'start_date', 'end_date'])
	serial_num = params['params']['serial_num']
	a_gas_sensor = GasSensor(serial_num)
	gas_sensors.load_to_device(a_gas_sensor)

	return a_gas_sensor.get_all_values_date_range({
			'start' : utls.parse_time(params['params']['start_date']), 
			'end' : utls.parse_time(params['params']['end_date'])
		})


@gas_sensor.route('/last_request_time', methods=['POST'])
def last_request_time():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_gas_sensor = GasSensor(serial_num)
	gas_sensors.load_to_device(a_gas_sensor)

	return a_gas_sensor.get_last_request_time()


@gas_sensor.route('/get_gas_value', methods=['POST'])
def get_gas_value():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_gas_sensor = GasSensor(serial_num)
	gas_sensors.load_to_device(a_gas_sensor)

	return a_gas_sensor.get_current_value()


@gas_sensor.route('/from_device', methods=['POST'])
def from_device():
	params = utls.get_input_params(request.data, ['serial_num', 'state', 'gas_val',
	'max_gas_value', 'slave_server', 'measurement_delay', 'conn_reist_trails',
	'buzz_duration', 'buzz_interval', 'R_0'])
	serial_num = params['params']['serial_num']
	state = params['params']['state']
	gas_val = float(params['params']['gas_val'])
	a_gas_sensor = GasSensor(serial_num)
	gas_sensors.load_to_device(a_gas_sensor)

	# Update the last request received
	update_req_res = a_gas_sensor.update_request_time()
	if not update_req_res['success']:
		return update_req_res

	gas_value_res = a_gas_sensor.enter_gas_value(gas_val)
	if not gas_value_res['success']:
		return gas_value_res

	# Insert state if different from the current state
	if state != a_gas_sensor.get_state():
		enter_state_res = a_gas_sensor.enter_new_state(state)
		if not enter_state_res['success']:
			return enter_state_res

	gas_sensors.add_device_params(serial_num, a_gas_sensor.to_dict())

	return update_req_res


@gas_sensor.route('/device_settings', methods=['POST'])
def device_settings():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_gas_sensor = GasSensor(serial_num)
	gas_sensors.load_to_device(a_gas_sensor)

	return a_gas_sensor.get_device_settings()




