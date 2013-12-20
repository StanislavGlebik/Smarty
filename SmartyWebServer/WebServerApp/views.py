import socket
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
import json
import ast

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

#TODO: remove hardcode
def send_request_to_device_manager(json_request):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 1313))
    s.sendall(json_request)
    response = s.recv(4096)
    return response

def get_device_list():
    return send_request_to_device_manager('{"action": "get_device_list"}')

def send_get_state(deviceId):
    return send_request_to_device_manager('{"action": "get_state", "deviceId": %s}'%deviceId)
    
def get_map():
    return send_request_to_device_manager('{"action": "get_map"}')

def get_smarty_state():
    return send_request_to_device_manager('{"action": "get_smarty_state"}')

# for clients
def get_state_for_client(request, deviceId):
    return HttpResponse(send_get_state(deviceId))

def get_map_for_client(request):
    return HttpResponse(get_map())

def index(request):
    devices = ast.literal_eval(get_device_list())
    smarty_state = ast.literal_eval(get_smarty_state())

    context = {'deviceList': devices,
               'startTime': smarty_state['start_time']}

    devicesStatus = []
    for device in smarty_state['devices_load_status']:
        devicesStatus.append(DeviceState(device[0], device[1], device[2]))

    context['devicesStatus'] = devicesStatus

    return render(request, 'WebServerApp/index.html', context)

def map(request):
    devices = ast.literal_eval(get_device_list())
    context = {'deviceList': devices}
    map = ast.literal_eval(get_map())

    rectanglesList = []
    for rect in map['rectangles']:
        rectanglesList.append(Rect(rect[0], rect[1], rect[2], rect[3]))

    deviceCoordinatesList = []
    for id in map['devicesCoordinates']:
        device = map['devicesCoordinates'][id]
        deviceCoordinatesList.append(DeviceCoordinate(device[0], device[1], name=devices[id], id=id))

    map['rectangles'] = rectanglesList
    map['devicesCoordinates'] = deviceCoordinatesList
    context.update(map)

    return render(request, 'WebServerApp/map.html', context)


def getTemperature(request, deviceId):

    message = json.loads(send_get_state(deviceId))
    devices = ast.literal_eval(get_device_list())

    context = {'deviceList': devices}
    if message["result"] == 1:
        context['temperature'] = message['temperature']
    else:
        context['temperature'] = message['error_msg']

    return render(request, 'WebServerApp/temperature.html', context)
