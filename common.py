import os

DRIVER_COMMON_MODULE_NAME="DriverCommon"
DRIVERS_FOLDER="drivers"
CONFIGS_FOLDER="configs"
CONFIGS_FILENAME="devices.json"
LOGGING_CONF="logging.conf"
PORT=1313

def getDevicesConfigFilePath():
	return os.path.join(CONFIGS_FOLDER, CONFIGS_FILENAME)

