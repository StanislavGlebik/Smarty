import unittest
import os
import sys
import json
import logging.config

try:
	mainProjectFolder = os.environ['SMARTY_MAIN_FOLDER']
except KeyError as e:
	mainProjectFolder = ".."

sys.path.append(mainProjectFolder)

import common
from DeviceManager import DeviceManager

class DriverManagerUnitTest_A(unittest.TestCase):
	def setUp(self):
		self.testFolder = "test_A"
		loggingConfFolder = os.path.join(common.CONFIGS_FOLDER, common.LOGGING_CONF)
		logging.config.fileConfig(os.path.join(self.testFolder, loggingConfFolder))	
		self.deviceManager = DeviceManager(os.path.join(self.testFolder, common.getDevicesConfigFilePath()),
									  os.path.join(mainProjectFolder, common.DRIVERS_FOLDER))

	#getDeviceList() checking
	def testA(self):
		deviceList = self.deviceManager.getDeviceList()
		deviceList.sort()
		assert [(0, "Temperature sensor")] == deviceList

	#sendCommand() checking
	def testB(self):
		deviceList = self.deviceManager.getDeviceList()
		deviceId = deviceList[0][0]
		result  = self.deviceManager.sendCommand(json.loads('{"get_temperature":"", "deviceId": 0}'))
		assert "{'temperature': 15}" == result

if __name__ == "__main__":
    unittest.main()