from flask import Blueprint, request
import json
import time

from hidden_server.controls import Socket3x, Devices
from .. import views_utls as utls


socket3x = Blueprint('socket3x', __name__, url_prefix='/socket3x')

sockets = Devices('socket3x')


@socket3x.route('/get_current_state', methods=['POST'])
def get_current_state():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_socket = Socket3x(serial_num)
	sockets.load_to_device(a_socket)
	return a_socket.get_current_state()


@socket3x.route('/get_current_states', methods=['POST'])
def get_current_states():
	states = {}
	params = utls.get_input_params(request.data, ['serial_nums'])
	for serial_num in params['params']['serial_nums']:
		a_socket = Socket3x(serial_num)
		sockets.load_to_device(a_socket)
		states[serial_num] = a_socket.get_current_state()

	return states


@socket3x.route('/get_all_states_in_range', methods=['POST'])
def get_all_states_in_range():
	params = utls.get_input_params(request.data, ['serial_num', 'start_date', 'end_date'])
	serial_num = params['params']['serial_num']
	a_socket = Socket3x(serial_num)
	sockets.load_to_device(a_socket)

	return a_socket.get_all_states_date_range({
			'start' : utls.parse_time(params['params']['start_date']), 
			'end' : utls.parse_time(params['params']['end_date'])
		})


@socket3x.route('/last_request_time', methods=['POST'])
def last_request_time():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_socket = Socket3x(serial_num)
	sockets.load_to_device(a_socket)

	return a_socket.get_last_request_time()


@socket3x.route('/enter_requested_action', methods=['POST'])
def enter_requested_action():
	params = utls.get_input_params_all(request.data)
	serial_num = params['params']['serial_num']
	a_socket = Socket3x(serial_num)
	sockets.load_to_device(a_socket)
	del params['params']['serial_num']
	enter_result = a_socket.enter_new_request(params['params'])
	sockets.add_device_params(serial_num, a_socket.to_dict())
	
	return enter_result


@socket3x.route('/last_requested_action', methods=['POST'])
def last_requested_action():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_socket = Socket3x(serial_num)
	sockets.load_to_device(a_socket)
	return a_socket.get_last_record()


@socket3x.route('/requested_actions_in_range', methods=['POST'])
def requested_actions_in_range():
	params = utls.get_input_params(request.data, ['serial_num', 'start_date', 'end_date'])
	serial_num = params['params']['serial_num']
	a_socket = Socket3x(serial_num)
	sockets.load_to_device(a_socket)

	return a_socket.get_all_actions_date_range({
			'start' : utls.parse_time(params['params']['start_date']),
			'end' : utls.parse_time(params['params']['end_date'])
		})


@socket3x.route('/from_device', methods=['POST'])
def from_device():
	params = utls.get_input_params(request.data, ['serial_num', 'state_left', 'state_center', 'state_right'])
	serial_num = params['params']['serial_num']
	states = {}
	states['left'] = params['params']['state_left']
	states['center'] = params['params']['state_center']
	states['right'] = params['params']['state_right']
	a_socket = Socket3x(serial_num)
	sockets.load_to_device(a_socket)

	# Update the last request received
	update_req_res = a_socket.update_request_time()
	if not update_req_res['success']:
		return update_req_res

	# Insert state if different from the current state
	if states != a_socket.get_states():
		enter_state_res = a_socket.enter_new_states(states)
		if not enter_state_res['success']:
			return enter_state_res
	
	# Update if requested action is taken
	last_req_action = a_socket.get_last_record()	
	if not last_req_action['success']:
		return last_req_action

	seen_fields = []
	actions_taken = {}
	for k, v in last_req_action.items():
		side = k.split('_')[-1]
		if side in ['left', 'center', 'right'] and not k in seen_fields:
			action_req = 'action_requested_' + side
			action_taken = 'action_taken_' + side
			if last_req_action[action_req] == states[side]:
				if last_req_action[action_taken] == 'NO':
					actions_taken[action_taken] = 'YES'

			seen_fields.extend([action_req, action_taken])

	# Update actions taken field
	if actions_taken != {}:
		update_actions_res = a_socket.update_actions(actions_taken)
		if not update_actions_res['success']:
			return update_actions_res

	last_req_action.update(actions_taken)	
	sockets.add_device_params(serial_num, a_socket.to_dict())

	return last_req_action


@socket3x.route('/device_settings', methods=['POST'])
def device_settings():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_socket = Socket3x(serial_num)
	sockets.load_to_device(a_socket)
	return a_socket.get_device_settings()