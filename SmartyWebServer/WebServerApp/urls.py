from django.conf.urls import patterns, url
from WebServerApp import views

urlpatterns = patterns('',
    url(r'getTemperature/$', views.getTemperature, name='getTemperature')
)