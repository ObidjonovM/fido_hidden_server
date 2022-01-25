from flask import Blueprint, request
import json
import time

from hidden_server.controls import WiFiLock, Devices
from .. import views_utls as utls


wifi_lock = Blueprint('wifi_lock', __name__, url_prefix='/wifi_lock')

wifi_locks = Devices('wifi_lock')


@wifi_lock.route('/get_current_state', methods=['POST'])
def get_current_state():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_wifi_lock = WiFiLock(serial_num)
	wifi_locks.load_to_device(a_wifi_lock)
	return a_wifi_lock.get_current_state()


@wifi_lock.route('/get_current_states', methods=['POST'])
def get_current_states():
	states = {}
	params = utls.get_input_params(request.data, ['serial_nums'])
	for serial_num in params['params']['serial_nums']:
		a_wifi_lock = WiFiLock(serial_num)
		wifi_locks.load_to_device(a_wifi_lock)
		states[serial_num] = a_wifi_lock.get_current_state()

	return states


@wifi_lock.route('/get_all_states_in_range', methods=['POST'])
def get_all_states_in_range():
	params = utls.get_input_params(request.data, ['serial_num', 'start_date', 'end_date'])
	serial_num = params['params']['serial_num']
	a_wifi_lock = WiFiLock(serial_num)
	wifi_locks.load_to_device(a_wifi_lock)

	return a_wifi_lock.get_all_states_date_range({
			'start' : utls.parse_time(params['params']['start_date']), 
			'end' : utls.parse_time(params['params']['end_date'])
		})


@wifi_lock.route('/last_request_time', methods=['POST'])
def last_request_time():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_wifi_lock = WiFiLock(serial_num)
	wifi_locks.load_to_device(a_wifi_lock)
	
	return a_wifi_lock.get_last_request_time()


@wifi_lock.route('/enter_requested_action', methods=['POST'])
def enter_requested_action():
	params = utls.get_input_params(request.data, ['serial_num', 'action_requested'])
	serial_num = params['params']['serial_num']
	a_wifi_lock = WiFiLock(serial_num)
	wifi_locks.load_to_device(a_wifi_lock)
	enter_result = a_wifi_lock.enter_new_request(params['params']['action_requested'])
	wifi_locks.add_device_params(serial_num, a_wifi_lock.to_dict())

	return enter_result


@wifi_lock.route('/last_requested_action', methods=['POST'])
def last_requested_action():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_wifi_lock = WiFiLock(serial_num)
	wifi_locks.load_to_device(a_wifi_lock)

	return a_wifi_lock.get_last_record()


@wifi_lock.route('/requested_actions_in_range', methods=['POST'])
def requested_actions_in_range():
	params = utls.get_input_params(request.data, ['serial_num', 'start_date', 'end_date'])
	serial_num = params['params']['serial_num']
	a_wifi_lock = WiFiLock(serial_num)
	wifi_locks.load_to_device(a_wifi_lock)

	return a_wifi_lock.get_all_actions_date_range({
			'start' : utls.parse_time(params['params']['start_date']),
			'end' : utls.parse_time(params['params']['end_date'])
		})


@wifi_lock.route('/from_device', methods=['POST'])
def from_device():
	params = utls.get_input_params(request.data, ['serial_num', 'state'])
	serial_num = params['params']['serial_num']
	state = params['params']['state']
	a_wifi_lock = WiFiLock(serial_num)
	wifi_locks.load_to_device(a_wifi_lock)

	# Update the last request received
	update_req_res = a_wifi_lock.update_request_time()
	if not update_req_res['success']:
		return update_req_res

	# Insert state if different from the current state
	if state != a_wifi_lock.get_state():
		enter_state_res = a_wifi_lock.enter_new_state(state)
		if not enter_state_res['success']:
			return enter_state_res

	# Update if requested action is taken
	last_req_action = a_wifi_lock.get_last_record()
	
	if not last_req_action['success']:
		return last_req_action

	if last_req_action['action_requested'] == state:
		if last_req_action['action_taken'] == 'NO':
			
			# Update action taken field
			update_action_res = a_wifi_lock.update_action('YES')
			if not update_action_res['success']:
				return update_action_res

			last_req_action['action_taken'] = 'YES'

	wifi_locks.add_device_params(serial_num, a_wifi_lock.to_dict())

	return last_req_action


@wifi_lock.route('/device_settings', methods=['POST'])
def device_settings():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_wifi_lock = WiFiLock(serial_num)
	wifi_locks.load_to_device(a_wifi_lock)

	return a_wifi_lock.get_device_settings()