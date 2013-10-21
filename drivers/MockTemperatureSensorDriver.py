import DriverCommon

class MockTemperatureSensorDriver:	
	def __init__(self, config):
		pass

	def doIt(self, params):
		if params.has_key("get_temperature"):
			return "{'temperature': 15}"
		else:
			raise DriverCommon.DriverException("Bad command")
