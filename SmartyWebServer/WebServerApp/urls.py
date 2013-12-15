from django.conf.urls import patterns, url
from WebServerApp import views

urlpatterns = patterns('',
	url(r'^$', views.index),
	url(r'map', views.map),
    url(r'getTemperature/(?P<deviceId>\d+)$', views.getTemperature, name='getTemperature')
)