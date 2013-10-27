import DriverCommon

class MockTemperatureSensorDriver:	
	def __init__(self, config):
		if config.has_key("name"):
			self.name = config["name"]
		else:
			self.name = "No name"

	def doIt(self, params):
		if params.has_key("get_temperature"):
			return '{"temperature": 15}'
		else:
			raise DriverCommon.DriverException("Bad command")
