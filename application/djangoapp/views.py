from django.http import HttpResponseRedirect
from django.http import HttpResponse
from apipkg import api_manager as api
from apipkg import queue_manager as queue
from application.djangoapp.models import *
from django.shortcuts import render
from .forms import ArticleForm
from django.http import JsonResponse
from django.core import serializers
from .models import Article
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json
from datetime import datetime, timedelta
import requests
import random
import os

### IHM ###

def index(request):
    if request.method == 'POST' and request.FILES['file']:
        json_data = request.FILES['file'].read()
        try:
            is_json = json.loads(json_data)
        except ValueError:
            return render(request, 'index.html', {"error" : "Le fichier n'est pas au bon format"})
        else:
            send = api.post_request('catalogue-produit', 'load-data', json_data)
            return HttpResponseRedirect('/info')
    else:
        return render(request, 'index.html', {})


def info(request):
    produits = Produit.objects.all()
    context = {'produits' : produits}
    return render(request, 'info.html', context)

### Data Loading and Clearing ###

@csrf_exempt
def load_data(request):
    json_data = json.loads(request.body)
    new_products = []
    for product in json_data["produits"]:
        prix_fournisseur = product["prix"] * 100
        prix_vente = int(prix_fournisseur * 1.3)
        exclusivite = get_exclusivite()
        defaults = {"familleProduit" : product["familleProduit"], "descriptionProduit" : product["descriptionProduit"], "quantiteMin" : product["quantiteMin"], "packaging" : product["packaging"], "prix" : prix_vente, "prixFournisseur" : prix_fournisseur, "exclusivite" : exclusivite}
        new_product, created = Produit.objects.update_or_create(codeProduit=product["codeProduit"],  defaults=defaults)
        if created:
            new_products.append(model_to_dict(new_product))
    if len(new_products) > 0:
        send_gesco_new_products({ "produits" : new_products})
    return HttpResponse(json.dumps(json_data))

@csrf_exempt
def automatic_load_data(request):
    json_file = open('tests/data.json')
    json_data = json.load(json_file)
    send = api.post_request('catalogue-produit', 'load-data', json.dumps(json_data))
    json_file.close()
    return HttpResponse("OK")

def schedule_load_data(request):
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(days=1)
    api.schedule_task('catalogue-produit','automatic-load-data', time, 'day', '{}', 'catalogue-produit','automatic_load_db')
    return HttpResponseRedirect('/info')

def clear_data(request):
    deleted = Produit.objects.all().delete()
    return HttpResponseRedirect('info')

### API ###

def api_get_all(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed()
    produits = Produit.objects.all()

    filtered = filter(produits, request.GET.get('familleProduit', False))

    json_data = list(filtered.values())
    return JsonResponse({ "produits" : json_data})

def api_get_ecommerce(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed()
    produits = Produit.objects.exclude(exclusivite__exact="magasin")

    filtered = filter(produits, request.GET.get('familleProduit', False))

    json_data = list(filtered.values())
    return JsonResponse({"produits": json_data})

def api_get_magasin(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed()
    produits = Produit.objects.exclude(exclusivite__exact="ecommerce")

    filtered = filter(produits, request.GET.get('familleProduit', False))

    json_data = list(filtered.values())
    return JsonResponse({"produits": json_data})

def api_get_by_id(request, code_produit):
    if request.method != 'GET':
        return HttpResponseNotAllowed()
    if (code_produit):
        try:
            produit = Produit.objects.get(codeProduit=code_produit)
        except Produit.DoesNotExist:
            return JsonResponse({'error': 'Code produit invalide ou produit inexistant'}, status=404)
        else:
            return JsonResponse({'produit' : model_to_dict(produit)})
    else:
        return JsonResponse({'error': 'Veuillez spécifier un code produit'}, status=400)

### ASYNC MESSAGES ###
def send_gesco_new_products(products):
    products["functionname"] = "catalogue-add-product"
    to =  "gestion-commerciale"
    time = api.send_request('scheduler', 'clock/time')
    message = { "from" : os.environ['DJANGO_APP_NAME'], "to" : to, "datetime" : time, "body" : products}
    queue.send(to, json.dumps(message))
    return


### ASYNC FILES ###

def write_catalogue_to_file(request):
    return send_catalogue_file("crm")

def send_catalogue_file(destination_app):
    with open("catalogue.json", "w+") as f:
        produits = Produit.objects
        if destination_app == "ecommerce":
            produits = produits.exclude(exclusivite__exact="magasin")
        elif destination_app == "magasin":
            produits = produits.exclude(exclusivite__exact="ecommerce")
        else:
            produits = produits.all()
        json_data = list(produits.values())
        json_data = {"produits" : json_data}
        f.write(json.dumps(json_data))
        r = requests.post('http://127.0.0.1:5001/send', data={'me': os.environ['DJANGO_APP_NAME'],
                                                              'app': destination_app,
                                                              'path': 'catalogue.json'})
    return HttpResponse(r.text)     

### SIMULATEUR ###
def simulateur(request):
    return api.send_request('simulateur', 'control/catalog')


### FILTERS ###
def filter(query_set, familleProduit):
    if (familleProduit):
        query_set = query_set.filter(familleProduit__exact=familleProduit)
    return query_set

### HELPERS ###
def get_exclusivite():
    val = random.random() * 100
    if val < 50:
        return ''
    elif val < 75:
        return 'ecommerce'
    else:
        return 'magasin'

