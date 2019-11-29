import os
import requests
import json
from datetime import datetime, timedelta

from django.apps import AppConfig
from apipkg import api_manager as api

myappurl = "http://localhost:" + os.environ["WEBSERVER_PORT"]

class ApplicationConfig(AppConfig):
    name = 'application.djangoapp'

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            name = os.environ['DJANGO_APP_NAME']
            scheduler_reset_url = '/app/delete?source=' + name
            status_code = api.post_request('scheduler', scheduler_reset_url, '{}')
            api.unregister(name)
            api.register(myappurl, name)
            clock_time = api.send_request('scheduler', 'clock/time')
            time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
            time = time + timedelta(days=1)
            api.schedule_task('catalogue-produit','load-from-fournisseur', time, 'day', '{}', 'catalogue-produit','load_products_from_supplier')

            

