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

def index(request):
    if request.method == 'POST' and request.FILES['file']:
        json_data = request.FILES['file'].read()
        send = api.post_request('catalogue-produit', 'load-data', json_data)
        return HttpResponseRedirect('/info')
    else:
        return render(request, 'index.html', {})


def info(request):
    produits = Produit.objects.all()
    context = {'produits' : produits}
    return render(request, 'info.html', context)

def schedule_load_data(request):
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(seconds=10)
    #data = {'host' : 'catalogue-produit', 'url' : 'catalogueproduit/load-data', 'recurrence' : 'minute', 'data' : json_data, 'source' : 'catalogue-produit', 'name' : 'Chargement automatique du catalogue produit'}
    #send = api.post_request('scheduler', 'schedule/add')
    schedule_task('catalogue-produit','automatic-load-data', time, 'minute', '{}', 'catalogue-produit','automatic_load_db')
    return HttpResponseRedirect('/info')

@csrf_exempt
def load_data(request):
    Produit.objects.all().delete()
    json_data = json.loads(request.body)
    for product in json_data["produits"]:
        rounded_price = product["prix"] * 100
        new_product = Produit(codeProduit=product["codeProduit"], familleProduit=product["familleProduit"], descriptionProduit=product["descriptionProduit"], quantiteMin=product["quantiteMin"], packaging=product["packaging"], prix=rounded_price)
        new_product.save()
    return HttpResponse(json.dumps(json_data))

@csrf_exempt
def automatic_load_data(request):
    json_file = open('tests/data.json')
    json_data = json.load(json_file)
    send = api.post_request('catalogue-produit', 'load-data', json.dumps(json_data))
    json_file.close()
    return HttpResponse("OK")

def api_data(request):
    id = request.GET.get('id')
    if (id):
        # If one article is specified, try to retrieve this one
        try:
            produit = Produit.objects.get(id=id)
        except Produit.DoesNotExist:
            return JsonResponse({'error': 'ID produit invalide ou produit inexistant'}, status=404)
        else:
            return JsonResponse({'produit' : model_to_dict(produit)})
    else:
        # If no id is specified, return every product
        produits = list(Produit.objects.all().values())
        return JsonResponse({'produits' : produits})

def clear_data(request):
    deleted = Produit.objects.all().delete()
    return HttpResponseRedirect('info')

def schedule_task(host, url, time, recurrence, data, source, name):
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    headers = {'Host': 'scheduler'}
    data = {"target_url": url, "target_app": host, "time": time_str, "recurrence": recurrence, "data": data, "source_app": source, "name": name}
    r = requests.post(api.api_services_url + 'schedule/add', headers = headers, json = data)
    print(r.status_code)
    print(r.text)
    return r.text
