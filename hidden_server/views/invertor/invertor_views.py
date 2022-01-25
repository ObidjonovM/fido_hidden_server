from flask import Blueprint, request
import json
import time

from hidden_server.controls import Invertor, Devices
from .. import views_utls as utls


invertor = Blueprint('invertor', __name__, url_prefix='/invertor')

invertors = Devices('invertor')


@invertor.route('/get_current_state', methods=['POST'])
def get_current_state():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	an_invertor = Invertor(serial_num)
	invertors.load_to_device(an_invertor)
	
	return an_invertor.get_current_state()


@invertor.route('/get_current_states', methods=['POST'])
def get_current_states():
	states = {}
	params = utls.get_input_params(request.data, ['serial_nums'])

	for serial_num in params['params']['serial_nums']:
		an_invertor = Invertor(serial_num)
		invertors.load_to_device(an_invertor)
		states[serial_num] = an_invertor.get_current_state()

	return states


@invertor.route('/get_all_states_in_range', methods=['POST'])
def get_all_states_in_range():
	params = utls.get_input_params(request.data, ['serial_num', 'start_date', 'end_date'])
	serial_num = params['params']['serial_num']
	an_invertor = Invertor(serial_num)
	invertors.load_to_device(an_invertor)

	return an_invertor.get_all_states_date_range({
			'start' : utls.parse_time(params['params']['start_date']), 
			'end' : utls.parse_time(params['params']['end_date'])
		})


@invertor.route('/last_request_time', methods=['POST'])
def last_request_time():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	an_invertor = Invertor(serial_num)
	invertors.load_to_device(an_invertor)

	return an_invertor.get_last_request_time()


@invertor.route('/from_device', methods=['POST'])
def from_device():
	params = utls.get_input_params(request.data, ['serial_num', 'state'])
	serial_num = params['params']['serial_num']
	state = params['params']['state']
	an_invertor = Invertor(serial_num)
	invertors.load_to_device(an_invertor)

	# Update the last request received
	update_req_res = an_invertor.update_request_time()
	if not update_req_res['success']:
		return update_req_res

	# Insert state if different from the current state
	if state != an_invertor.get_state():
		enter_state_res = an_invertor.enter_new_state(state)
		if not enter_state_res['success']:
			return enter_state_res

	return update_req_res


@invertor.route('/device_settings', methods=['POST'])
def device_settings():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	an_invertor = Invertor(serial_num)
	invertors.load_to_device(an_invertor)

	return an_invertor.get_device_settings()