import DriverCommon

class MockTemperatureSensorDriver:	
	def __init__(self, config):
		if config.has_key("viewer"):
			self.viewer = config["viewer"]
		else:
			self.viewer = "default"

		if config.has_key("name"):
			self.name = config["name"]
		else:
			self.name = "No name"
		if config.has_key("temperature"):
			self.temperature = config["temperature"]
		else:
			self.temperature = 15

	def doIt(self, params):
		try:
			if params["action"] == "get_state":
				return '{"result":1, "temperature": %(temperature)s, "viewer": "%(viewer)s"}'%{'temperature': self.temperature, 'viewer': self.viewer}
			else:
				raise Exception()
		except :
			raise DriverCommon.DriverException("Bad command")
