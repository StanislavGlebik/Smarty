from django.db import models

class WeatherRecord(models.Model):
	date = models.DateTimeField()
	humidity = models.FloatField()
	temperature = models.FloatField()
