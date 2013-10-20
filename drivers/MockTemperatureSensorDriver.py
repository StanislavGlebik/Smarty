import DriverCommon

class MockTemperatureSensorDriver:	
	def doIt(self, params):
		if params.has_key("get_temperature"):
			return "{'temperature': 15}"
		else:
			raise DriverCommon.DriverException("Bad command")
