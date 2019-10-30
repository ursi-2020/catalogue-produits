import os
import requests
import json

from django.apps import AppConfig
from apipkg import api_manager as api

myappurl = "http://localhost:" + os.environ["WEBSERVER_PORT"]

class ApplicationConfig(AppConfig):
    name = 'application.djangoapp'

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            api.unregister(os.environ['DJANGO_APP_NAME'])
            api.register(myappurl, os.environ['DJANGO_APP_NAME'])
            

