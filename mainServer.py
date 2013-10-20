import os
import logging.config
import json

import socket
import common
import sys

logger = logging.getLogger("mainServerLogger")

deviceDrivers = []

def handleDevice(device):
	if not device.has_key("name"):
		logger.error("Bad name for device " + json.dumps(device))
	else:
		logger.info("Device " + device["name"] + " founded")

	if not device.has_key("driver"):
		logger.error("No driver name in " + json.dumps(device))
	else:
		try:
			deviceClass = getattr(__import__(device["driver"]), device["driver"])
			deviceDrivers.append(deviceClass())
		except ImportError as e:
			logger.error("Cannot load driver: " + e.message)
		else:
			logger.info("Driver was loaded")

def initDevices():
	if not os.path.exists(common.getDevicesConfigFilePath()):
		logger.error("No devices config files was found. Exiting.")
	else:
		logger.info("Configs files was found.")

	with open(common.getDevicesConfigFilePath(), "r") as configFile:
		try:
			devices = json.loads("".join(configFile.readlines()))
			for device in devices:
				handleDevice(device)
		except ValueError as e:
			logger.error("Bad json in devices.json: " + e.message + " Exiting.")
		except :
			logger.error("Unknown error")

def loop(serversocket):
	driverCommonModule = __import__(common.DRIVER_COMMON_MODULE_NAME)

	while True:
		(clientsocket, address) = serversocket.accept()
		logger.info("New connection: " + str(address))
		command = clientsocket.recv(4096)
		logger.info("Received command: " + command)
		try:
			clientsocket.send(deviceDrivers[0].doIt(json.loads(command)))
		except driverCommonModule.DriverException as e:
			clientsocket.send(e.message)
		except Exception as e:
			logger.error(e.message)

def main():
	sys.path.append(common.DRIVERS_FOLDER)
	logging.config.fileConfig(os.path.join("configs", "logging.conf"))
	logger.info("===============Start initialization===============")
	initDevices()

	try:
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serversocket.bind(('localhost', common.PORT))
		serversocket.listen(5)
		loop(serversocket)
	except Exception as e:
		logger.error(e.message)

if __name__ == '__main__':
	main()
