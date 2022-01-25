import sys
sys.path.append('..')
from config import db_credentials

import psycopg2


conn = psycopg2.connect(db_credentials)

cur = conn.cursor()


# creating socket_state table
cur.execute('''
CREATE TABLE IF NOT EXISTS socket_state (
	log_id INT PRIMARY KEY CHECK (log_id > 0),
	state_time TIMESTAMP NOT NULL,
	serial_num CHAR(12) NOT NULL,
	state VARCHAR(3) NOT NULL);
''')


# creating index for socket_state table
cur.execute('''
CREATE INDEX IF NOT EXISTS idx_socket_state_serial 
		ON socket_state(serial_num);
''')


# creating socket_request_times table
cur.execute('''
CREATE TABLE IF NOT EXISTS socket_request_times (
	serial_num CHAR(12) PRIMARY KEY,
	request_time TIMESTAMP NOT NULL);
''')


# creating socket_actions table
cur.execute('''
CREATE TABLE IF NOT EXISTS socket_actions (
	log_id INT PRIMARY KEY CHECK (log_id > 0),
	serial_num CHAR(12) NOT NULL,
	action_requested VARCHAR(3) NOT NULL,
	requested_time TIMESTAMP NOT NULL,
	action_taken VARCHAR(3) NOT NULL,
	action_time TIMESTAMP NOT NULL);
''')


# creating index for socket_actions table
cur.execute('''
CREATE INDEX IF NOT EXISTS idx_socket_actions_serial
		ON socket_actions(serial_num);
''')


# creating socket_settings table
cur.execute('''
CREATE TABLE IF NOT EXISTS socket_settings (
	serial_num CHAR(12) PRIMARY KEY,
	slave_server VARCHAR(200) NOT NULL,
	measurement_delay VARCHAR(14) NOT NULL,
	min_delay VARCHAR(14) NOT NULL,
	num_delays VARCHAR(14) NOT NULL,
	conn_reist_trails VARCHAR(14) NOT NULL,
	date_added TIMESTAMP NOT NULL,
	date_modified TIMESTAMP NOT NULL);
''')


# creating gas_sensor_state table
cur.execute('''
CREATE TABLE IF NOT EXISTS gas_sensor_state (
	log_id INT PRIMARY KEY CHECK (log_id > 0),
	state_time TIMESTAMP NOT NULL,
	serial_num CHAR(12) NOT NULL,
	state VARCHAR(3) NOT NULL);
''')


# creating index for gas_sensor_state table
cur.execute('''
CREATE INDEX IF NOT EXISTS idx_gas_sensor_state_serial 
		ON gas_sensor_state(serial_num);
''')


# creating gas_sensor_values table
cur.execute('''
CREATE TABLE IF NOT EXISTS gas_sensor_values (
	log_id INT PRIMARY KEY CHECK (log_id > 0),
	serial_num CHAR(12) NOT NULL,
	gas_value NUMERIC(12,2) NOT NULL,
	request_time TIMESTAMP NOT NULL);
''')


# creating index for gas_sensor_values table
cur.execute('''
CREATE INDEX IF NOT EXISTS idx_gas_sensor_values_serial 
		ON gas_sensor_values(serial_num);
''')


# creating gas_sensor_request_times table
cur.execute('''
CREATE TABLE IF NOT EXISTS gas_sensor_request_times (
	serial_num CHAR(12) PRIMARY KEY,
	request_time TIMESTAMP NOT NULL);
''')


# creating gas_sensor_settings table
cur.execute('''
CREATE TABLE IF NOT EXISTS gas_sensor_settings (
	serial_num CHAR(12) PRIMARY KEY,
	slave_server VARCHAR(200) NOT NULL,
	measurement_delay VARCHAR(14) NOT NULL,
	conn_reist_trails VARCHAR(14) NOT NULL,
	max_gas_value VARCHAR(14) NOT NULL,
	buzz_duration VARCHAR(14) NOT NULL,
	buzz_interval VARCHAR(14) NOT NULL,
	r_0 VARCHAR(14) NOT NULL,
	date_added TIMESTAMP NOT NULL,
	date_modified TIMESTAMP NOT NULL);
''')


# creating water_sensor table
cur.execute('''
CREATE TABLE IF NOT EXISTS water_sensor_state (
	log_id INT PRIMARY KEY CHECK (log_id > 0),
	state_time TIMESTAMP NOT NULL,
	serial_num CHAR(12) NOT NULL,
	state VARCHAR(3) NOT NULL);
''')


# creating index for water_sensor_state table
cur.execute('''
CREATE INDEX IF NOT EXISTS idx_water_sensor_state_serial 
		ON water_sensor_state(serial_num);
''')


# creating water_sensor_request_times table
cur.execute('''
CREATE TABLE IF NOT EXISTS water_sensor_request_times (
	serial_num CHAR(12) PRIMARY KEY,
	request_time TIMESTAMP NOT NULL);
''')


# creating water_sensor_settings table
cur.execute('''
CREATE TABLE IF NOT EXISTS water_sensor_settings (
	serial_num CHAR(12) PRIMARY KEY,
	slave_server VARCHAR(200) NOT NULL,
	measurement_delay VARCHAR(14) NOT NULL,
	conn_reist_trails VARCHAR(14) NOT NULL,
	buzz_duration VARCHAR(14) NOT NULL,
	buzz_interval VARCHAR(14) NOT NULL,
	date_added TIMESTAMP NOT NULL,
	date_modified TIMESTAMP NOT NULL);
''')


# creating fire_sensor table
cur.execute('''
CREATE TABLE IF NOT EXISTS fire_sensor_state (
	log_id INT PRIMARY KEY CHECK (log_id > 0),
	state_time TIMESTAMP NOT NULL,
	serial_num CHAR(12) NOT NULL,
	state VARCHAR(3) NOT NULL);
''')


# creating index for fire_sensor_state table
cur.execute('''
CREATE INDEX IF NOT EXISTS idx_fire_sensor_state_serial 
		ON fire_sensor_state(serial_num);
''')


# creating fire_sensor_request_times table
cur.execute('''
CREATE TABLE IF NOT EXISTS fire_sensor_request_times (
	serial_num CHAR(12) PRIMARY KEY,
	request_time TIMESTAMP NOT NULL);
''')


# creating fire_sensor_settings table
cur.execute('''
CREATE TABLE IF NOT EXISTS fire_sensor_settings (
	serial_num CHAR(12) PRIMARY KEY,
	slave_server VARCHAR(200) NOT NULL,
	measurement_delay VARCHAR(14) NOT NULL,
	conn_reist_trails VARCHAR(14) NOT NULL,
	max_gas_value VARCHAR(14) NOT NULL,
	buzz_duration VARCHAR(14) NOT NULL,
	buzz_interval VARCHAR(14) NOT NULL,
	date_added TIMESTAMP NOT NULL,
	date_modified TIMESTAMP NOT NULL);
''')


# creating gerkon table
cur.execute('''
CREATE TABLE IF NOT EXISTS gerkon_state (
	log_id INT PRIMARY KEY CHECK (log_id > 0),
	state_time TIMESTAMP NOT NULL,
	serial_num CHAR(12) NOT NULL,
	state VARCHAR(3) NOT NULL);
''')


# creating index for gerkon_state table
cur.execute('''
CREATE INDEX IF NOT EXISTS idx_gerkon_state_serial 
		ON gerkon_state(serial_num);
''')


# creating gerkon_request_times table
cur.execute('''
CREATE TABLE IF NOT EXISTS gerkon_request_times (
	serial_num CHAR(12) PRIMARY KEY,
	request_time TIMESTAMP NOT NULL);
''')


# creating gerkon_sensor_settings table
cur.execute('''
CREATE TABLE IF NOT EXISTS gerkon_settings (
	serial_num CHAR(12) PRIMARY KEY,
	slave_server VARCHAR(200) NOT NULL,
	measurement_delay VARCHAR(14) NOT NULL,
	conn_reist_trails VARCHAR(14) NOT NULL,
	buzz_duration VARCHAR(14) NOT NULL,
	buzz_interval VARCHAR(14) NOT NULL,
	date_added TIMESTAMP NOT NULL,
	date_modified TIMESTAMP NOT NULL);
''')


# creating vibration_sensor_state table
cur.execute('''
CREATE TABLE IF NOT EXISTS vibration_sensor_state (
	log_id INT PRIMARY KEY CHECK (log_id > 0),
	state_time TIMESTAMP NOT NULL,
	serial_num CHAR(12) NOT NULL,
	state VARCHAR(3) NOT NULL);
''')


# creating index for vibration_sensor_state table
cur.execute('''
CREATE INDEX IF NOT EXISTS idx_vibration_sensor_state_serial 
		ON vibration_sensor_state(serial_num);
''')


# creating vibration_sensor_request_times table
cur.execute('''
CREATE TABLE IF NOT EXISTS vibration_sensor_request_times (
	serial_num CHAR(12) PRIMARY KEY,
	request_time TIMESTAMP NOT NULL);
''')


#creating vibration_sensor_settings table
cur.execute('''
CREATE TABLE IF NOT EXISTS vibration_sensor_settings (
	serial_num CHAR(12) PRIMARY KEY,
	slave_server VARCHAR(200) NOT NULL,
	measurement_delay VARCHAR(14) NOT NULL,
	conn_reist_trails VARCHAR(14) NOT NULL,
	buzz_duration VARCHAR(14) NOT NULL,
	buzz_interval VARCHAR(14) NOT NULL,
	date_added TIMESTAMP NOT NULL,
	date_modified TIMESTAMP NOT NULL);
''')


# creating socket_button_state table
cur.execute('''
CREATE TABLE IF NOT EXISTS socket_button_state (
	log_id INT PRIMARY KEY CHECK (log_id > 0),
	state_time TIMESTAMP NOT NULL,
	serial_num CHAR(12) NOT NULL,
	state VARCHAR(3) NOT NULL);
''')


# creating index for socket_button_state table
cur.execute('''
CREATE INDEX IF NOT EXISTS idx_socket_button_state_serial 
		ON socket_button_state(serial_num);
''')


# creating socket_button_request_times table
cur.execute('''
CREATE TABLE IF NOT EXISTS socket_button_request_times (
	serial_num CHAR(12) PRIMARY KEY,
	request_time TIMESTAMP NOT NULL);
''')


# creating socket_button_actions table
cur.execute('''
CREATE TABLE IF NOT EXISTS socket_button_actions (
	log_id INT PRIMARY KEY CHECK (log_id > 0),
	serial_num CHAR(12) NOT NULL,
	action_requested VARCHAR(3) NOT NULL,
	requested_time TIMESTAMP NOT NULL,
	action_taken VARCHAR(3) NOT NULL,
	action_time TIMESTAMP NOT NULL);
''')


# creating index for socket_button_actions table
cur.execute('''
CREATE INDEX IF NOT EXISTS idx_socket_button_actions_serial
		ON socket_button_actions(serial_num);
''')


# creating socket_button_settings table
cur.execute('''
CREATE TABLE IF NOT EXISTS socket_button_settings (
	serial_num CHAR(12) PRIMARY KEY,
	slave_server VARCHAR(200) NOT NULL,
	measurement_delay VARCHAR(14) NOT NULL,
	min_delay VARCHAR(14) NOT NULL,
	num_delays VARCHAR(14) NOT NULL,
	conn_reist_trails VARCHAR(14) NOT NULL,
	date_added TIMESTAMP NOT NULL,
	date_modified TIMESTAMP NOT NULL);
''')


# creating invertor table
cur.execute('''
CREATE TABLE IF NOT EXISTS invertor_state (
	log_id INT PRIMARY KEY CHECK (log_id > 0),
	state_time TIMESTAMP NOT NULL,
	serial_num CHAR(12) NOT NULL,
	state VARCHAR(3) NOT NULL);
''')


# creating index for invertor_state table
cur.execute('''
CREATE INDEX IF NOT EXISTS idx_invertor_state_serial 
		ON invertor_state(serial_num);
''')


# creating invertor_request_times table
cur.execute('''
CREATE TABLE IF NOT EXISTS invertor_request_times (
	serial_num CHAR(12) PRIMARY KEY,
	request_time TIMESTAMP NOT NULL);
''')


# creating invertor_settings table
cur.execute('''
CREATE TABLE IF NOT EXISTS invertor_settings (
	serial_num CHAR(12) PRIMARY KEY,
	slave_server VARCHAR(200) NOT NULL,
	measurement_delay VARCHAR(14) NOT NULL,
	conn_reist_trails VARCHAR(14) NOT NULL,
	date_added TIMESTAMP NOT NULL,
	date_modified TIMESTAMP NOT NULL);
''')


# creating wifi_lock_state table
cur.execute('''
CREATE TABLE IF NOT EXISTS wifi_lock_state (
	log_id INT PRIMARY KEY CHECK (log_id > 0),
	state_time TIMESTAMP NOT NULL,
	serial_num CHAR(12) NOT NULL,
	state VARCHAR(10) NOT NULL);
''')


# creating index for wifi_lock_state table
cur.execute('''
CREATE INDEX IF NOT EXISTS idx_wifi_lock_state 
		ON wifi_lock_state(serial_num);
''')


# creating wifi_lock_request_times table
cur.execute('''
CREATE TABLE IF NOT EXISTS wifi_lock_request_times (
	serial_num CHAR(12) PRIMARY KEY,
	request_time TIMESTAMP NOT NULL);
''')


# creating wifi_lock_actions table
cur.execute('''
CREATE TABLE IF NOT EXISTS wifi_lock_actions (
	log_id INT PRIMARY KEY CHECK (log_id > 0),
	serial_num CHAR(12) NOT NULL,
	action_requested VARCHAR(10) NOT NULL,
	requested_time TIMESTAMP NOT NULL,
	action_taken VARCHAR(3) NOT NULL,
	action_time TIMESTAMP NOT NULL);
''')


# creating index for wifi_lock_actions table
cur.execute('''
CREATE INDEX IF NOT EXISTS idx_wifi_lock_actions_serial
		ON wifi_lock_actions(serial_num);
''')


# creating wifi_lock_settings table
cur.execute('''
CREATE TABLE IF NOT EXISTS wifi_lock_settings (
	serial_num CHAR(12) PRIMARY KEY,
	slave_server VARCHAR(200) NOT NULL,
	measurement_delay VARCHAR(14) NOT NULL,
	min_delay VARCHAR(14) NOT NULL,
	num_delays VARCHAR(14) NOT NULL,
	conn_reist_trails VARCHAR(14) NOT NULL,
	date_added TIMESTAMP NOT NULL,
	date_modified TIMESTAMP NOT NULL);
''')


# creating socket_3x_state table
cur.execute('''
CREATE TABLE IF NOT EXISTS socket_3x_state (
	log_id INT PRIMARY KEY CHECK (log_id > 0),
	state_time TIMESTAMP NOT NULL,
	serial_num CHAR(12) NOT NULL,
	state_left VARCHAR(3) NOT NULL,
	state_center VARCHAR(3) NOT NULL,
	state_right VARCHAR(3) NOT NULL);
''')


# creating index for socket_3x_state table
cur.execute('''
CREATE INDEX IF NOT EXISTS idx_socket_3x_state_serial 
		ON socket_3x_state(serial_num);
''')


# creating socket_3x_request_times table
cur.execute('''
CREATE TABLE IF NOT EXISTS socket_3x_request_times (
	serial_num CHAR(12) PRIMARY KEY,
	request_time TIMESTAMP NOT NULL);
''')


# creating socket_3x_actions table
cur.execute('''
CREATE TABLE IF NOT EXISTS socket_3x_actions (
	log_id INT PRIMARY KEY CHECK (log_id > 0),
	serial_num CHAR(12) NOT NULL,
	requested_time TIMESTAMP NOT NULL,
	action_requested_left VARCHAR(3) NOT NULL,
	action_requested_center VARCHAR(3) NOT NULL,
	action_requested_right VARCHAR(3) NOT NULL,
	requested_time_left TIMESTAMP NOT NULL,
	requested_time_center TIMESTAMP NOT NULL,
	requested_time_right TIMESTAMP NOT NULL,
	action_taken_left VARCHAR(3) NOT NULL,
	action_taken_center VARCHAR(3) NOT NULL,
	action_taken_right VARCHAR(3) NOT NULL,
	action_time_left TIMESTAMP NOT NULL,
	action_time_center TIMESTAMP NOT NULL,
	action_time_right TIMESTAMP NOT NULL);
''')


# creating index for socket_3x_actions table
cur.execute('''
CREATE INDEX IF NOT EXISTS idx_socket_3x_actions_serial
		ON socket_3x_actions(serial_num);
''')


# creating socket_3x_settings table
cur.execute('''
CREATE TABLE IF NOT EXISTS socket_3x_settings (
	serial_num CHAR(12) PRIMARY KEY,
	slave_server VARCHAR(200) NOT NULL,
	measurement_delay VARCHAR(14) NOT NULL,
	min_delay VARCHAR(14) NOT NULL,
	num_delays VARCHAR(14) NOT NULL,
	conn_reist_trails VARCHAR(14) NOT NULL,
	date_added TIMESTAMP NOT NULL,
	date_modified TIMESTAMP NOT NULL);
''')


# creating tuvak_measurements table
cur.execute('''
CREATE TABLE IF NOT EXISTS tuvak_measurements (
	log_id INT PRIMARY KEY CHECK (log_id > 0),
	serial_num CHAR(12) NOT NULL,
	soil_moist NUMERIC(12,2) NOT NULL,
	air_humid NUMERIC(12,2) NOT NULL,
	temp NUMERIC(12,2) NOT NULL,
	measured_time TIMESTAMP NOT NULL);
''')


# creating tuvak_state table
cur.execute('''
CREATE TABLE IF NOT EXISTS tuvak_state (
	log_id INT PRIMARY KEY CHECK (log_id > 0),
	state_time TIMESTAMP NOT NULL,
	serial_num CHAR(12) NOT NULL,
	state VARCHAR(3) NOT NULL);
''')


# creating index for tuvak_state table
cur.execute('''
CREATE INDEX IF NOT EXISTS idx_tuvak_state 
		ON tuvak_state(serial_num);
''')


# creating tuvak_request_times table
cur.execute('''
CREATE TABLE IF NOT EXISTS tuvak_request_times (
	serial_num CHAR(12) PRIMARY KEY,
	request_time TIMESTAMP NOT NULL);
''')


# creating tuvak_actions table
cur.execute('''
CREATE TABLE IF NOT EXISTS tuvak_actions (
	log_id INT PRIMARY KEY CHECK (log_id > 0),
	serial_num CHAR(12) NOT NULL,
	action_requested VARCHAR(3) NOT NULL,
	requested_time TIMESTAMP NOT NULL,
	action_taken VARCHAR(3) NOT NULL,
	action_time TIMESTAMP NOT NULL);
''')


# creating index for tuvak_actions table
cur.execute('''
CREATE INDEX IF NOT EXISTS idx_tuvak_actions
		ON tuvak_actions(serial_num);
''')


# creating tuvak_settings table
cur.execute('''
CREATE TABLE IF NOT EXISTS tuvak_settings (
	serial_num CHAR(12) PRIMARY KEY,
	slave_server VARCHAR(200) NOT NULL,
	measurement_delay VARCHAR(14) NOT NULL,
	pump_on_delay VARCHAR(14) NOT NULL,
	moist_samples VARCHAR(14) NOT NULL,
	conn_reist_trails VARCHAR(14) NOT NULL,
	max_soil_moist NUMERIC(12,2) NOT NULL,
	date_added TIMESTAMP NOT NULL,
	date_modified TIMESTAMP NOT NULL);
''')


cur.execute('''
CREATE TABLE IF NOT EXISTS error_logs (
	log_id INT PRIMARY KEY CHECK (log_id > 0),
        serial_num CHAR(12) NOT NULL,
        call_path TEXT NOT NULL,
        function_name VARCHAR(50) NOT NULL,
        line_number INT NOT NULL CHECK (line_number > 0),
        error_name VARCHAR(50) NOT NULL,
        description TEXT NOT NULL,
        date_added TIMESTAMP NOT NULL);
''')


conn.commit()

cur.close()

conn.close()