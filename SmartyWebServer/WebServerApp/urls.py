from django.conf.urls import patterns, url
from WebServerApp import views

urlpatterns = patterns('',
	url(r'^$', views.index),
    url(r'json/getmap', views.get_map_for_client),    
	url(r'^map$', views.map),
    url(r'getState/(?P<deviceId>\d+)$', views.getTemperature, name='getTemperature'),
    url(r'json/getstate/(?P<deviceId>.+)$', views.get_state_for_client)
)