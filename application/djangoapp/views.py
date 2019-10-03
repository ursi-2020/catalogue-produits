from django.http import HttpResponseRedirect
from django.http import HttpResponse
from apipkg import api_manager as api
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
    Produit.objects.all().delete()
    json_data = json.loads(request.body)
    for product in json_data["produits"]:
        rounded_price = product["prix"] * 100
        exclusivite = getExclusivite()
        new_product = Produit(codeProduit=product["codeProduit"], familleProduit=product["familleProduit"], descriptionProduit=product["descriptionProduit"], quantiteMin=product["quantiteMin"], packaging=product["packaging"], prix=rounded_price, exclusivite=exclusivite)
        new_product.save()
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
    time = time + timedelta(seconds=10)
    #data = {'host' : 'catalogue-produit', 'url' : 'catalogueproduit/load-data', 'recurrence' : 'minute', 'data' : json_data, 'source' : 'catalogue-produit', 'name' : 'Chargement automatique du catalogue produit'}
    #send = api.post_request('scheduler', 'schedule/add')
    schedule_task('catalogue-produit','automatic-load-data', time, 'minute', '{}', 'catalogue-produit','automatic_load_db')
    return HttpResponseRedirect('/info')

def clear_data(request):
    deleted = Produit.objects.all().delete()
    return HttpResponseRedirect('info')

### Scheduler Wrapper ###

def schedule_task(host, url, time, recurrence, data, source, name):
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    headers = {'Host': 'scheduler'}
    data = {"target_url": url, "target_app": host, "time": time_str, "recurrence": recurrence, "data": data, "source_app": source, "name": name}
    r = requests.post(api.api_services_url + 'schedule/add', headers = headers, json = data)
    print(r.status_code)
    print(r.text)
    return r.text

### API ###

def api_get_all(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed();
    produits = Produit.objects.all()

    filtered = filter(produits, request.GET.get('familleProduit', False))

    json_data = list(filtered.values())
    return JsonResponse({ "produits" : json_data})

def api_get_ecommerce(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed();
    produits = Produit.objects.exclude(exclusivite__exact="magasin")

    filtered = filter(produits, request.GET.get('familleProduit', False))

    json_data = list(filtered.values())
    return JsonResponse({"produits": json_data})

def api_get_magasin(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed();
    produits = Produit.objects.exclude(exclusivite__exact="ecommerce")

    filtered = filter(produits, request.GET.get('familleProduit', False))

    json_data = list(filtered.values())
    return JsonResponse({"produits": json_data})

def api_get_by_id(request, id_product):
    if request.method != 'GET':
        return HttpResponseNotAllowed();
    if (id_product):
        try:
            produit = Produit.objects.get(id=id_product)
        except Produit.DoesNotExist:
            return JsonResponse({'error': 'ID produit invalide ou produit inexistant'}, status=404)
        else:
            return JsonResponse({'produit' : model_to_dict(produit)})
    else:
        return JsonResponse({'error': 'Veuillez spécifier un ID'}, status=400)

### FILTERS ###
def filter(query_set, familleProduit):
    if (familleProduit):
        query_set = query_set.filter(familleProduit__exact=familleProduit)
    return query_set

### HELPERS ###
def getExclusivite():
    val = random.random() * 100
    if val < 50:
        return ''
    elif val < 75:
        return 'ecommerce'
    else:
        return 'magasin'

