from flask import Flask
from .views import (socket, gas_sensor, water_sensor, fire_sensor, gerkon,
	vibration_sensor, socket_button, invertor, wifi_lock, socket3x, tuvak)



app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'         # IMPORTANT!!!! *** change before deploying to production ***

app.register_blueprint(socket)
app.register_blueprint(gas_sensor)
app.register_blueprint(water_sensor)
app.register_blueprint(fire_sensor)
app.register_blueprint(gerkon)
app.register_blueprint(vibration_sensor)
app.register_blueprint(socket_button)
app.register_blueprint(invertor)
app.register_blueprint(wifi_lock)
app.register_blueprint(socket3x)
app.register_blueprint(tuvak)
