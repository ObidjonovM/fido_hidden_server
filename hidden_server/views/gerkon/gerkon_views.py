from flask import Blueprint, request
import json
import time

from hidden_server.controls import Gerkon, Devices
from .. import views_utls as utls


gerkon = Blueprint('gerkon', __name__, url_prefix='/gerkon')

gerkons = Devices('gerkon')


@gerkon.route('/get_current_state', methods=['POST'])
def get_current_state():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_gerkon = Gerkon(serial_num)
	gerkons.load_to_device(a_gerkon)
	
	return a_gerkon.get_current_state()


@gerkon.route('/get_current_states', methods=['POST'])
def get_current_states():
	states = {}
	params = utls.get_input_params(request.data, ['serial_nums'])

	for serial_num in params['params']['serial_nums']:
		a_gerkon = Gerkon(serial_num)
		gerkons.load_to_device(a_gerkon)
		states[serial_num] = a_gerkon.get_current_state()

	return states


@gerkon.route('/get_all_states_in_range', methods=['POST'])
def get_all_states_in_range():
	params = utls.get_input_params(request.data, ['serial_num', 'start_date', 'end_date'])
	serial_num = params['params']['serial_num']
	a_gerkon = Gerkon(serial_num)
	gerkons.load_to_device(a_gerkon)

	return a_gerkon.get_all_states_date_range({
			'start' : utls.parse_time(params['params']['start_date']), 
			'end' : utls.parse_time(params['params']['end_date'])
		})


@gerkon.route('/last_request_time', methods=['POST'])
def last_request_time():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_gerkon = Gerkon(serial_num)
	gerkons.load_to_device(a_gerkon)

	return a_gerkon.get_last_request_time()


@gerkon.route('/from_device', methods=['POST'])
def from_device():
	params = utls.get_input_params(request.data, ['serial_num', 'state'])
	serial_num = params['params']['serial_num']
	state = params['params']['state']
	a_gerkon = Gerkon(serial_num)
	gerkons.load_to_device(a_gerkon)

	# Update the last request received
	update_req_res = a_gerkon.update_request_time()
	if not update_req_res['success']:
		return update_req_res

	# Insert state if different from the current state
	if state != a_gerkon.get_state():
		enter_state_res = a_gerkon.enter_new_state(state)
		if not enter_state_res['success']:
			return enter_state_res

	return update_req_res


@gerkon.route('/device_settings', methods=['POST'])
def device_settings():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_gerkon = Gerkon(serial_num)
	gerkons.load_to_device(a_gerkon)

	return a_gerkon.get_device_settings()