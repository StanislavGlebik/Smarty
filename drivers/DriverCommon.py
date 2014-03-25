class DriverException(Exception):
	pass

class CommonDriver:
	def __init__(self, config):
		if config.has_key("viewer"):
			self.viewer = config["viewer"]
		else:
			self.viewer = "default"