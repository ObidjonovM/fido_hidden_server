from flask import Blueprint, request
import json
from hidden_server.controls import Tuvak, Devices
from .. import views_utls as utls


tuvak = Blueprint('tuvak', __name__, url_prefix='/tuvak')

tuvaks = Devices('tuvak')


@tuvak.route('/get_current_state', methods=['POST'])
def get_current_state():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_tuvak = Tuvak(serial_num)
	tuvaks.load_to_device(a_tuvak)
	return a_tuvak.get_current_state()


@tuvak.route('/get_current_states', methods=['POST'])
def get_current_states():
	states = {}
	params = utls.get_input_params(request.data, ['serial_nums'])
	for serial_num in params['params']['serial_nums']:
		a_tuvak = Tuvak(serial_num)
		tuvaks.load_to_device(a_tuvak)
		states[serial_num] = a_tuvak.get_current_state()

	return states


@tuvak.route('/get_all_states_in_range', methods=['POST'])
def get_all_states_in_range():
	params = utls.get_input_params(request.data, ['serial_num', 'start_date', 'end_date'])
	serial_num = params['params']['serial_num']
	a_tuvak = Tuvak(serial_num)
	tuvaks.load_to_device(a_tuvak)

	return a_tuvak.get_all_states_date_range({
			'start' : utls.parse_time(params['params']['start_date']), 
			'end' : utls.parse_time(params['params']['end_date'])
		})


@tuvak.route('/last_request_time', methods=['POST'])
def last_request_time():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_tuvak = Tuvak(serial_num)
	tuvaks.load_to_device(a_tuvak)
	
	return a_tuvak.get_last_request_time()


@tuvak.route('/enter_requested_action', methods=['POST'])
def enter_requested_action():
	params = utls.get_input_params(request.data, ['serial_num', 'action_requested'])
	serial_num = params['params']['serial_num']
	a_tuvak = Tuvak(serial_num)
	tuvaks.load_to_device(a_tuvak)
	enter_result = a_tuvak.enter_new_request(params['params']['action_requested'])
	tuvaks.add_device_params(serial_num, a_tuvak.to_dict())

	return enter_result


@tuvak.route('/last_requested_action', methods=['POST'])
def last_requested_action():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_tuvak = Tuvak(serial_num)
	tuvaks.load_to_device(a_tuvak)

	return a_tuvak.get_last_record()


@tuvak.route('/requested_actions_in_range', methods=['POST'])
def requested_actions_in_range():
	params = utls.get_input_params(request.data, ['serial_num', 'start_date', 'end_date'])
	serial_num = params['params']['serial_num']
	a_tuvak = Tuvak(serial_num)
	tuvaks.load_to_device(a_tuvak)

	return a_tuvak.get_all_actions_date_range({
			'start' : utls.parse_time(params['params']['start_date']),
			'end' : utls.parse_time(params['params']['end_date'])
		})


@tuvak.route('/enter_measurement', methods=['POST'])
def enter_measurement():
	params = utls.get_input_params(
			request.data, 
			['serial_num', 'soil_moist', 'air_humid', 'temp', 'measured_time'])

	serial_num = params['params']['serial_num']
	a_tuvak = Tuvak(serial_num)
	tuvaks.load_to_device(a_tuvak)
	enter_result = a_tuvak.enter_measurement(params['params'])
	tuvaks.add_device_params(serial_num, a_tuvak.to_dict())

	return enter_result


@tuvak.route('/get_last_measurement', methods=['POST'])
def get_last_measurement():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_tuvak = Tuvak(serial_num)
	tuvaks.load_to_device(a_tuvak)

	return a_tuvak.get_last_measurement()


@tuvak.route('/get_all_measurements_date_range', methods=['POST'])
def get_all_measurements_date_range():
	params = utls.get_input_params(
			request.data, 
			['serial_num', 'start_date', 'end_date'])

	serial_num = params['params']['serial_num']
	a_tuvak = Tuvak(serial_num)
	tuvaks.load_to_device(a_tuvak)

	return a_tuvak.get_all_measurements_date_range({
			'start' : utls.parse_time(params['params']['start_date']), 
			'end' : utls.parse_time(params['params']['end_date'])
		})


@tuvak.route('/from_device', methods=['POST'])
def from_device():
	params = utls.get_input_params(
			request.data, 
			['serial_num', 'water_poured', 'soil_moist', 'air_humid', 'temp',
			'slave_server', 'measurement_delay', 'conn_reist_trails',
			'pump_on_delay', 'moist_samples'])

	serial_num = params['params']['serial_num']
	water_poured = params['params']['water_poured']
	params['params'].pop('water_poured')

	a_tuvak = Tuvak(serial_num)
	tuvaks.load_to_device(a_tuvak)

	# Update the last request received
	update_req_res = a_tuvak.update_request_time()
	if not update_req_res['success']:
		return update_req_res

	enter_result = a_tuvak.enter_measurement(params['params'])

	if not enter_result['success']:
		return enter_result

	# Update if requested action is taken
	last_req_action = a_tuvak.get_last_record()

	if not last_req_action['success']:
		return last_req_action

	if water_poured == 'YES':
		# Update action taken field
		update_action_res = a_tuvak.update_action('YES')
		if not update_action_res['success']:
			return update_action_res

		last_req_action['action_taken'] = 'YES'

	tuvaks.add_device_params(serial_num, a_tuvak.to_dict())

	return last_req_action


@tuvak.route('/device_settings', methods=['POST'])
def device_settings():
	params = utls.get_input_params(request.data, ['serial_num'])
	serial_num = params['params']['serial_num']
	a_tuvak = Tuvak(serial_num)
	tuvaks.load_to_device(a_tuvak)

	return a_tuvak.get_device_settings()