import os
import logging.config
import json

import socket
import common
import sys

from DeviceManager import DeviceManager

logger = logging.getLogger("mainServerLogger")

def loop(serversocket, deviceManager):
	while True:
		(clientsocket, address) = serversocket.accept()
		logger.info("New connection: " + str(address))
		command = clientsocket.recv(4096)
		logger.info("Received command: " + command)
		try:
			clientsocket.sendall(deviceManager.sendCommand(json.loads(command)))
		except driverCommonModule.DriverException as e:
			clientsocket.sendall(e.message)
		except Exception as e:
			logger.error(e.message)

def main():
	logging.config.fileConfig(os.path.join(common.CONFIGS_FOLDER, common.LOGGING_CONF))
	logger.info("===============Start initialization===============")

	deviceManager = DeviceManager(common.getDevicesConfigFilePath(), common.DRIVERS_FOLDER)

	try:
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serversocket.bind(('localhost', common.PORT))
		serversocket.listen(5)
		loop(serversocket, deviceManager)
	except Exception as e:
		logger.error(e.message)

if __name__ == '__main__':
	main()
