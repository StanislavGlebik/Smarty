import socket
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

def get_device_list():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #TODO: remove hardcode!!!
    s.connect(('localhost', 1313))
    s.sendall('{"action": "get_device_list"}')
    devices = s.recv(4096)
    devices = ast.literal_eval(devices)

    return devices

def get_map():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 1313))

    s.sendall('{"action": "get_map"}')
    map = s.recv(4096)
    map = ast.literal_eval(map)

    return map

def index(request):
    devices = get_device_list()
    context = {'deviceList': devices}

    return render(request, 'WebServerApp/index.html', context)

def map(request):
    devices = get_device_list()
    context = {'deviceList': devices}
    map = get_map()

    rectanglesList = []
    for rect in map['rectangles']:
        rectanglesList.append(Rect(rect[0], rect[1], rect[2], rect[3]))
    map['rectangles'] = rectanglesList

    context.update(map)

    return render(request, 'WebServerApp/map.html', context)

#TODO: remove hardcode
def getTemperature(request, deviceId):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 1313))

    s.sendall('{"action": "get_temperature", "deviceId": %s}'%deviceId)
    message = s.recv(4096)
    print message
    message = json.loads(message)
    devices = get_device_list()

    context = {'temperature': message['temperature'],
                'deviceList': devices}

    return render(request, 'WebServerApp/temperature.html', context)