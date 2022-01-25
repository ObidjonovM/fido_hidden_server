import os

db_credentials = 'dbname=your_db user=your_login password=your_password'

LOGS_PATH = 'logs'

if not os.path.exists(LOGS_PATH):
	os.mkdir(LOGS_PATH)