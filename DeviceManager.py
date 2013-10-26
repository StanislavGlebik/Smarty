import logging
import json
import os
import sys

import common

#Logger name: deviceManagerLogger
class DeviceManager:
	def __init__(self, configFile, driverModulesFolder):
		sys.path.append(driverModulesFolder)
		self.logger = logging.getLogger("deviceManagerLogger")
		self.logger.addHandler(logging.NullHandler())
		self.__allLoadedDevices = {}
		self.__initDevices(configFile)

	def getDeviceList(self):
		return [(id, device.name) for (id, device) in self.__allLoadedDevices.items()]

	def sendCommand(self, command):
		driverCommonModule = __import__(common.DRIVER_COMMON_MODULE_NAME)
		try:
			device = self.__allLoadedDevices[command["deviceId"]]
			return device.doIt(command)		
		except driverCommonModule.DriverException as e:
			self.logger.error("Error while handling request: " + e.message)
			return self.__getJSONError("Error while handling request: " + e.message)
		except KeyError as e:
			self.logger.error("Bad id!")
			return self.__getJSONError("Bad id!")

	def __getJSONError(self, message):
		#TODO: format string
		#TODO: error codes
		return "['Bad request': '" + message + "']"

	def __initDevices(self, configFile):
		if not os.path.exists(configFile):
			self.logger.error("No devices config files was found. Stop initialization.")
			raise Exception("Couldn't find device config file")
		else:
			self.logger.info("Configs files was found.")

		with open(configFile, "r") as configFile:
			try:
				devices = json.loads("".join(configFile.readlines()))
				for deviceConfig in devices:
					self.__handleDevice(deviceConfig)
			except ValueError as e:
				self.logger.error("Bad json in devices.json: " + e.message + " Exiting.")
			except Exception as e:
				self.logger.error(e.message)

	def __handleDevice(self, deviceConfig):
		if not deviceConfig.has_key("driver"):
			self.logger.error("No driver name in " + json.dumps(deviceConfig))
			return
		else:
			try:
				deviceDriverClass = getattr(__import__(deviceConfig["driver"]), deviceConfig["driver"])
				self.__allLoadedDevices[self.__getNewDeviceId()] = deviceDriverClass(deviceConfig)
			except ImportError as e:
				self.logger.error("Cannot load driver: " + e.message)
			else:
				self.logger.info("Driver was loaded")

	def __getNewDeviceId(self):
		return len(self.__allLoadedDevices)
