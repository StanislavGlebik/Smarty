from django.shortcuts import render
from WebServerApp.models import WeatherRecord

from datetime import datetime

TEMPLATE_NAME = 'WebServerApp/temperature.html'

def render_tmpl(request, message, context):
    print message
    if message["result"] == 1:
        context['temperature'] = message['temperature']
    else:
        context['temperature'] = message['error_msg']

    rec = WeatherRecord(date = datetime.now(), humidity=0.3, temperature=24.0)
    rec.save()
    
    return render(request, TEMPLATE_NAME, context)
