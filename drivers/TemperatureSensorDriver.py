import DriverCommon
from pyDHT import DHTReader

class TemperatureSensorDriver:	
	def __init__(self, config):
		if config.has_key("viewer"):
			self.viewer = config["viewer"]
		else:
			self.viewer = "default"

		if config.has_key("name"):
			self.name = config["name"]
		else:
			self.name = "No name"

		if config.has_key("pin"):
			self.pin = config["pin"]
		else:
			self.pin = 4
	
		if config.has_key("temp_sensor_type"):
			self.pin = config["temp_sensor_type"]
		else:
			self.pin = 11

		self.dht_reader = DHTReader()

	def doIt(self, params):
		#try:
		if params["action"] == "get_state":
			temp = -1
			while temp == -1:
				temp, hum = self.dht_reader.get_temperature()
			return '{"result": 1, "temperature": %(temperature)s, "viewer": "%(viewer)s"}'%{'temperature': temp, 'viewer': self.viewer}
		else:
			raise Exception("troubles with handling request")
		#except :
			#raise DriverCommon.DriverException("Bad command")
