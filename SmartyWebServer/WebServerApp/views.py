import socket
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext, loader
from models import ExerciseType, SportExercise
import datetime
import json
import ast

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

class SportEvent:
	def __init__(self, date, activity):
		self.date = date
		self.activity = activity

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
    
def get_map(floor):
    return send_request_to_device_manager('{"action": "get_map", "floor": %s}'%floor)

def get_smarty_state():
    return send_request_to_device_manager('{"action": "get_smarty_state"}')

def get_floors_amount():
    return send_request_to_device_manager('{"action": "get_floors_amount"}')

# for clients
def get_state_for_client(request, deviceId):
    return HttpResponse(send_get_state(deviceId))

def get_map_for_client(request):
    return HttpResponse(get_map())

@general_info_decorator
def index(request, devices, floorList):
    smarty_state = ast.literal_eval(get_smarty_state())

    context = {'deviceList': devices,
               'floors': floorList,
               'startTime': smarty_state['start_time']}

    devicesStatus = []
    for device in smarty_state['devices_load_status']:
        devicesStatus.append(DeviceState(device[0], device[1], device[2]))
    
    context['devicesStatus'] = devicesStatus

    return render(request, 'WebServerApp/index.html', context)

@general_info_decorator
def map(request, devices, floorList, floor):
    context = {'deviceList': devices,
               'floors': floorList}

    map = ast.literal_eval(get_map(floor))

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

@general_info_decorator
def get_device_state(request, devices, floorList, deviceId):
    message = json.loads(send_get_state(deviceId))

    context = {'deviceList': devices,
               'floors': floorList} 

    if message["result"] == 1:
        context['temperature'] = message['temperature']
    else:
        context['temperature'] = message['error_msg']

    return render(request, 'WebServerApp/temperature.html', context)

@general_info_decorator
def about(request, devices, floorList):
    context = {'deviceList': devices,
               'floors': floorList}

    return render(request, 'WebServerApp/about.html', context)

@general_info_decorator
def sport_diary(request, devices, floorList):
    events = [SportEvent(x.training_date, x.exercise.activity) for x in SportExercise.objects.all()]

    context = {'deviceList': devices,
               'floors': floorList,
               'events': events}

    return render(request, 'WebServerApp/sportdiary.html', context)

@general_info_decorator
def add_sport_event(request, devices, floorList):
    if request.method == "GET":
        exercises = [x.activity for x in ExerciseType.objects.all()]
    	today = datetime.date.today()
        context = {'deviceList': devices,
                   'floors': floorList,
                   'exercises': exercises,
               	   'curDate': today.strftime("%Y-%m-%d")}

        return render(request, 'WebServerApp/addsportevent.html', context)
    elif request.method == "POST":
        date = request.POST['date']
        exerciseName = request.POST['exerciseName']
        exercise = get_object_or_404(ExerciseType, activity=exerciseName)
        newExercise = SportExercise(training_date=date, exercise=exercise)
        newExercise.save()
        return redirect('/addsportevent')
    else:
        raise Http404
