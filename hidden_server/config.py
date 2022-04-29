import os
from pymongo import MongoClient


CLIENT = MongoClient("mongodb://localhost:27017/")
HIDDEN_DB = CLIENT["your_db"]

LOGS_PATH = 'logs'

if not os.path.exists(LOGS_PATH):
	os.mkdir(LOGS_PATH)