from django.http import HttpResponse
from apipkg import api_manager as api


def index(request):
    app_info = api.send_request('gestioncommerciale', 'info')
    return HttpResponse("Je suis Catalogue Produits et je demande un truc à %r" % app_info)

def info(request):
	return HttpResponse("Catalogue Produits")