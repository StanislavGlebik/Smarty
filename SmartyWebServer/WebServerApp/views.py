from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext, loader
import json
import ast
import sys
import os
import importlib

from viewsCommon import general_info_decorator
from viewsCommon import send_request_to_device_manager
from viewsCommon import get_map
from viewsCommon import send_get_state
from viewsCommon import get_smarty_state
from viewsCommon import DeviceState
from viewsCommon import Rect
from viewsCommon import DeviceCoordinate

from viewsCommon import CommonNames

# for clients
def get_state_for_client(request, deviceId):
    return HttpResponse(send_get_state(deviceId))

def get_map_for_client(request):
    return HttpResponse(get_map())

@general_info_decorator
def index(request, devices, floorList):
    smarty_state = ast.literal_eval(get_smarty_state())

    context = {CommonNames.DEVICES_LIST: devices,
               CommonNames.FLOORS_LIST: floorList,
               CommonNames.SMARTY_START_TIME: smarty_state['start_time']}

    devicesStatus = []
    for device in smarty_state['devices_load_status']:
        devicesStatus.append(DeviceState(device[0], device[1], device[2]))
    
    context[CommonNames.DEVICES_STATUS_LIST] = devicesStatus

    return render(request, 'WebServerApp/index.html', context)

@general_info_decorator
def map(request, devices, floorList, floor):
    context = {CommonNames.DEVICES_LIST: devices,
               CommonNames.FLOORS_LIST: floorList}

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

    context = {CommonNames.DEVICES_LIST: devices,
               CommonNames.FLOORS_LIST: floorList} 

    if (message.has_key(CommonNames.VIEWER_KEY)):
        viewerModule = importlib.import_module(message[CommonNames.VIEWER_KEY])
        return viewerModule.render_tmpl(request, message, context)
    else:
        #TODO: default view
        return render(request, 'WebServerApp/default.html', context)

@general_info_decorator
def about(request, devices, floorList):
    context = {CommonNames.DEVICES_LIST: devices,
               CommonNames.FLOORS_LIST: floorList}

    return render(request, 'WebServerApp/about.html', context)
