import socket
from django.http import HttpResponse

def getTemperature(request):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#remove hardcode!!!
	s.connect(('localhost', 1313))
	s.send('{"get_temperature":""}')
	message = s.recv(4096)
	return HttpResponse(message)