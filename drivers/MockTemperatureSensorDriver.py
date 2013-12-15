import DriverCommon

class MockTemperatureSensorDriver:	
	def __init__(self, config):
		if config.has_key("name"):
			self.name = config["name"]
		else:
			self.name = "No name"

	def doIt(self, params):
		try:
			if params["action"] == "get_state":
				return '{"result":1, "temperature": 15}'
			else:
				raise Exception()
		except :
			raise DriverCommon.DriverException("Bad command")
