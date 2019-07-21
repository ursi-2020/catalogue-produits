from django.http import HttpResponse
from apipkg import api_manager as api
from application.djangoapp.models import *

def index(request):
    time = api.send_request('scheduler', 'clock/time')
    return HttpResponse("L'heure de la clock est %r" % time)

def info(request):
    return HttpResponse(Article.objects.all())

def info_gestion_commerciale(request):
    info_gestion_commerciale = api.send_request('gestioncommerciale', 'gestioncommerciale/info')
    return HttpResponse("Voici les infos envoyées par la gestion commerciale : %r" % info_gestion_commerciale)