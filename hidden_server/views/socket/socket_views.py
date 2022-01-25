from flask import Blueprint, request
import json
import time

from hidden_server.controls import Socket, Devices
from .. import views_utls as utls


socket = Blueprint('socket', __name__, url_prefix='/socket')

sockets = Devices('socket')


@socket.route('/get_current_state', methods=['POST'])
def get_current_state():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_socket = Socket(serial_num)
	sockets.load_to_device(a_socket)
	return a_socket.get_current_state()


@socket.route('/get_current_states', methods=['POST'])
def get_current_states():
	states = {}
	params = utls.get_input_params(request.data, ['serial_nums'])
	for serial_num in params['params']['serial_nums']:
		a_socket = Socket(serial_num)
		sockets.load_to_device(a_socket)
		states[serial_num] = a_socket.get_current_state()

	return states


@socket.route('/get_all_states_in_range', methods=['POST'])
def get_all_states_in_range():
	params = utls.get_input_params(request.data, ['serial_num', 'start_date', 'end_date'])
	serial_num = params['params']['serial_num']
	a_socket = Socket(serial_num)
	sockets.load_to_device(a_socket)

	return a_socket.get_all_states_date_range({
			'start' : utls.parse_time(params['params']['start_date']), 
			'end' : utls.parse_time(params['params']['end_date'])
		})


@socket.route('/last_request_time', methods=['POST'])
def last_request_time():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_socket = Socket(serial_num)
	sockets.load_to_device(a_socket)
	
	return a_socket.get_last_request_time()


@socket.route('/enter_requested_action', methods=['POST'])
def enter_requested_action():
	params = utls.get_input_params(request.data, ['serial_num', 'action_requested'])
	serial_num = params['params']['serial_num']
	a_socket = Socket(serial_num)
	sockets.load_to_device(a_socket)
	enter_result = a_socket.enter_new_request(params['params']['action_requested'])
	sockets.add_device_params(serial_num, a_socket.to_dict())

	return enter_result


@socket.route('/last_requested_action', methods=['POST'])
def last_requested_action():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_socket = Socket(serial_num)
	sockets.load_to_device(a_socket)

	return a_socket.get_last_record()


@socket.route('/requested_actions_in_range', methods=['POST'])
def requested_actions_in_range():
	params = utls.get_input_params(request.data, ['serial_num', 'start_date', 'end_date'])
	serial_num = params['params']['serial_num']
	a_socket = Socket(serial_num)
	sockets.load_to_device(a_socket)

	return a_socket.get_all_actions_date_range({
			'start' : utls.parse_time(params['params']['start_date']),
			'end' : utls.parse_time(params['params']['end_date'])
		})


@socket.route('/from_device', methods=['POST'])
def from_device():
	params = utls.get_input_params(request.data, ['serial_num', 'state'])
	serial_num = params['params']['serial_num']
	state = params['params']['state']
	a_socket = Socket(serial_num)
	sockets.load_to_device(a_socket)

	# Update the last request received
	update_req_res = a_socket.update_request_time()
	if not update_req_res['success']:
		return update_req_res

	# Insert state if different from the current state
	if state != a_socket.get_state():
		enter_state_res = a_socket.enter_new_state(state)
		if not enter_state_res['success']:
			return enter_state_res

	# Update if requested action is taken
	last_req_action = a_socket.get_last_record()
	
	if not last_req_action['success']:
		return last_req_action

	if last_req_action['action_requested'] == state:
		if last_req_action['action_taken'] == 'NO':
			
			# Update action taken field
			update_action_res = a_socket.update_action('YES')
			if not update_action_res['success']:
				return update_action_res

			last_req_action['action_taken'] = 'YES'

	sockets.add_device_params(serial_num, a_socket.to_dict())

	return last_req_action


@socket.route('/device_settings', methods=['POST'])
def device_settings():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_socket = Socket(serial_num)
	sockets.load_to_device(a_socket)

	return a_socket.get_device_settings()