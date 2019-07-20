from django.http import HttpResponse
from apipkg import api_manager as api


def index(request):
    appli_info = api.send_request('bouchongestioncommerciale', 'info')
    return HttpResponse("Bienvenue dans le catalogue, petit message de la gestion commerciale : %r" % appli_info)

def info(request):
    return HttpResponse("Je suis le catalogue produit")
