#encoding=utf-8

from WebServerApp.models import *

rec = WeatherRecord(date='2014-04-14', humidity=0.3, temperature=24.0)
rec.save()

rec = WeatherRecord(date='2014-04-15', humidity=0.3, temperature=18.0)
rec.save()

rec = WeatherRecord(date='2014-04-16', humidity=0.3, temperature=19.0)
rec.save()

rec = WeatherRecord(date='2014-04-17', humidity=0.3, temperature=21.0)
rec.save()

rec = WeatherRecord(date='2014-04-18', humidity=0.3, temperature=22.0)
rec.save()

rec = WeatherRecord(date='2014-04-19', humidity=0.3, temperature=20.0)
rec.save()

rec = WeatherRecord(date='2014-04-20', humidity=0.3, temperature=20.0)
rec.save()

rec = WeatherRecord(date='2014-04-21', humidity=0.3, temperature=23.0)
rec.save()
