import socket
from django.http import HttpResponse
from django.template import RequestContext, loader
import json

def getTemperature(request):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #remove hardcode!!!
    s.connect(('localhost', 1313))
    s.sendall('{"get_temperature":"", "deviceId": 0}')
    message = s.recv(4096)

    message = json.loads(message)
    template = loader.get_template('WebServerApp/temperature.html')
    context = RequestContext(request, {
        'temperature': message['temperature'],
    })

    return HttpResponse(template.render(context))