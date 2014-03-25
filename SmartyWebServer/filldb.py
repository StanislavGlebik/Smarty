#encoding=utf-8

from WebServerApp.models import *

rec = WeatherRecord(date='2014-03-25', humidity=0.3, temperature=24.0)
rec.save()

