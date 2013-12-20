import logging
import json
import os
import sys
from time import gmtime, strftime

import common


#Logger name: deviceManagerLogger
class DeviceManager:
	def __init__(self, configFile, driverModulesFolder):
		sys.path.append(driverModulesFolder)
		self.logger = logging.getLogger("deviceManagerLogger")
		self.logger.addHandler(logging.NullHandler())
		self.startTime = gmtime()
		self.__allLoadedDevices = {}
		self.__devicesLoadStatus = []
		self.__deviceCoordinates = {}
		self.__devicesFloors = {}
		self.__initDevices(configFile)
		self.__readMap()

	def getDeviceList(self):
		return {id: device.name for (id, device) in self.__allLoadedDevices.items()}

	def __readMap(self):
		self.map = {}

		with open(common.getMapFilePath(), "r") as fin:
			self.floorsAmount = int(fin.readline())
			for i in range(self.floorsAmount):
				width, height = fin.readline().split()
				rectangles = []
				devices = []
				line = fin.readline()

				#TODO: Hack! Remove it!
				while line.startswith("Rect"):
					splitted = line.split()
					if len(splitted) > 0 and splitted[0] == "Rect":
						new_rect = (int(splitted[1]), int(splitted[2]), int(splitted[3]), int(splitted[4]))
						rectangles.append(new_rect)
					line = fin.readline()

				self.map[i] = {'width': width, 'height': height, 'rectangles': rectangles}

	def getMap(self, floor):
		def filterFunc(id):
			device = self.__devicesFloors[id]
			return (self.__devicesFloors.has_key(id) and (self.__devicesFloors[id] == floor))

		return {'rectangles': self.map[floor]['rectangles'],
				'width': self.map[floor]['width'],
				'height': self.map[floor]['height'],
				'devicesCoordinates': {id: self.__deviceCoordinates[id] for id in filter(filterFunc, self.__deviceCoordinates)}} 

	def getSmartyState(self):
		return {'start_time': strftime("%Y-%m-%d %H:%M:%S", self.startTime),
				'devices_load_status': self.__devicesLoadStatus}

	#TODO: remove hardcoded commands
	def sendCommand(self, command):
		driverCommonModule = __import__(common.DRIVER_COMMON_MODULE_NAME)
		if not command.has_key("action"):
			self.logger.error("No 'action' field in JSON " + json.dumps(command))
			return self.__getJSONError("No 'action' field in JSON " + json.dumps(command))

		if command["action"] == "get_device_list":
			return str(self.getDeviceList())

		try:
			if command["action"] == "get_map":
				return str(self.getMap(int(command["floor"])))
		except Exception as e:
			self.logger.error("Cannot get map: " + e.message)
			return self.__getJSONError("Error while handling request: " + e.message)

		if command["action"] == "get_floors_amount":
			return "[%d]"%self.floorsAmount

		try:
			if command["action"] == "get_smarty_state":
				return str(self.getSmartyState())
		except Exception as e:
			self.logger.error("Cannot get Smarty state" + e.message)
			return self.__getJSONError("Error while handling request: " +  e.message)

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
		#TODO: error codes
		return "{'result': 0, 'error_msg': '{%s}'}"%message

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
				deviceId = self.__getNewDeviceId()
				if deviceConfig.has_key("coordinates"):
					self.__deviceCoordinates[deviceId] = deviceConfig["coordinates"]
				if deviceConfig.has_key("floor"):
					self.__devicesFloors[deviceId] = deviceConfig["floor"]

				#TODO: add to status
				deviceDriverClass = getattr(__import__(deviceConfig["driver"]), deviceConfig["driver"])
				self.__allLoadedDevices[deviceId] = deviceDriverClass(deviceConfig)
			except ImportError as e:
				self.__devicesLoadStatus.append((deviceConfig["name"], "Failed", "No driver found"))
				self.logger.error("Cannot load driver, no driver found: " + e.message)
			except Exception as e:
				self.__devicesLoadStatus.append((deviceConfig["name"], "Failed", "Initialization troubles: " + e.message))
				self.logger.error("Cannot load driver, initialization troubles: " + e.message)			
			else:
				self.__devicesLoadStatus.append((deviceConfig["name"], "Success", ""))				
				self.logger.info("Driver was loaded " + deviceConfig["name"])

	def __getNewDeviceId(self):
		return len(self.__allLoadedDevices)
