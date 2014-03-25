import socket
import ast

class CommonNames:
	DEVICES_LIST = 'deviceList'
	FLOORS_LIST = 'floors'
	SMARTY_START_TIME = 'startTime'
	DEVICES_STATUS_LIST = 'devicesStatus'
	VIEWER_KEY = "viewer"

#TODO: remove hardcode
def send_request_to_device_manager(json_request):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 1313))
    s.sendall(json_request)
    response = s.recv(4096)
    return response

def get_device_list():
    return send_request_to_device_manager('{"action": "get_device_list"}')

def get_floors_amount():
    return send_request_to_device_manager('{"action": "get_floors_amount"}')

def general_info_decorator(handler):
	class Wrapper:
		def __init__(self, handler):
			self.handler = handler
			self.devices = ast.literal_eval(get_device_list())
			floors = ast.literal_eval(get_floors_amount())[0]
			self.floorList = range(floors)

		def __call__(self, request, **params):
			return handler(request, self.devices, self.floorList, **params)

	return Wrapper(handler)

class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class DeviceCoordinate(Rect):
    def __init__(self, x, y, id, name, width = 20, height = 20):
        Rect.__init__(self, x, y, width, height)
        self.id = id
        self.name = name

class DeviceState:
    def __init__(self, deviceName, status, reason=""):
        self.deviceName = deviceName
        self.status = status
        self.reason = reason

def send_get_state(deviceId):
    return send_request_to_device_manager('{"action": "get_state", "deviceId": %s}'%deviceId)
    
def get_map(floor):
    return send_request_to_device_manager('{"action": "get_map", "floor": %s}'%floor)

def get_smarty_state():
    return send_request_to_device_manager('{"action": "get_smarty_state"}')
