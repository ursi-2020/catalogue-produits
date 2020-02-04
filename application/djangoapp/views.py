from django.http import HttpResponseRedirect
from django.http import HttpResponse
from apipkg import api_manager as api
from apipkg import queue_manager as queue
from application.djangoapp.models import *
from django.shortcuts import render
from .forms import ArticleForm
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from .models import Article
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.utils.timezone import make_aware
import json
from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime
import requests
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
    produits = Produit.objects.all().order_by('codeProduit')
    try:
        date_raw = Log.objects.latest('date').date
        last_update = date_raw.strftime('%d/%m/%Y')
    except Log.DoesNotExist:
        last_update = 'None'
    context = {'produits' : produits, 'last_update' : last_update}
    return render(request, 'info.html', context)

### Data Loading and Clearing ###

@csrf_exempt
def load_data(request):
    json_data = json.loads(request.body)
    new_products = []
    nbModified, nbCreated = (0, 0)
    clock_time = api.send_request('scheduler', 'clock/time').strip('"')
    time = datetime.strptime(clock_time, '%d/%m/%Y-%H:%M:%S')
    for product in json_data["produits"]:
        # TODO: Ajouter le nom du fournisseur de manière dynamique
        nomFournisseur = "fo"
        #codeProduit = "%s-%s" % (nomFournisseur, product["codeProduit"])
        codeProduit = product["codeProduit"]
        prix_fournisseur = product["prix"] * 100
        prix_vente = int(prix_fournisseur * 1.5)
        defaults = {"codeProduitFournisseur": product["codeProduit"], "nomFournisseur": nomFournisseur, "familleProduit" : product["familleProduit"], "descriptionProduit" : product["descriptionProduit"], "quantiteMin" : product["quantiteMin"], "packaging" : product["packaging"], "prix" : prix_vente, "prixFournisseur" : prix_fournisseur}
        unchanged = { "dateCreation" : make_aware(time) }
        new_product, created = my_update_or_create(codeProduit, defaults, unchanged)
        if created:
            new_products.append(model_to_dict(new_product))
            nbCreated += 1
        else:
            nbModified += 1
    if nbCreated > 0:
        send_gesco_new_products({ "produits" : new_products})
    # LOG THE TRANSACTIONS
    new_log = Log(date=make_aware(time), nbCreated=nbCreated, nbModified=nbModified)
    new_log.save()
    ### Send catalogue as file to ecommerce
    send_catalogue_file('ecommerce')
    return JsonResponse(model_to_dict(new_log))

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

def clear_logs(request):
    deleted = Log.objects.all().delete()
    return JsonResponse({ "result" : "OK"})
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

def api_get_products_by_file(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed()
    destination_app = request.GET.get('app', False)
    if (destination_app):
        return send_catalogue_file(destination_app)
    return JsonResponse({'error': "Veuillez specifier votre nom d'application"}, status=400)

### SIMULATEUR API ###
def api_simulateur_get_all_ecommerce(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed()
    produits = list(Produit.objects.exclude(exclusivite__exact="magasin").values('codeProduit', 'codeProduitFournisseur', 'nomFournisseur'))
    return JsonResponse({ 'produits' : produits })

def api_simulateur_get_by_code(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed()
    nomFournisseur = request.GET.get('nomFournisseur', False)
    codeProduitFournisseur = request.GET.get('codeProduitFournisseur', False)
    if (not nomFournisseur):
        return JsonResponse({ "error" : "Missing nomFournisseur in query parameter"}, status=400)
    if (not codeProduitFournisseur):
        return JsonResponse({ "error" : "Missing codeProduitFournisseur in query parameter"}, status=400)
    try:
        produit = model_to_dict(Produit.objects.get(codeProduitFournisseur=codeProduitFournisseur, nomFournisseur=nomFournisseur))
    except Produit.DoesNotExist:
        return JsonResponse({'error': 'Produit inexistant'}, status=404)
    else:
        return JsonResponse({'produit' : {"codeProduit" : produit["codeProduit"],
                                          "codeProduitFournisseur" : produit["codeProduitFournisseur"],
                                          "nomFournisseur" : produit["nomFournisseur"],
                                          "exclusivite" : produit["exclusivite"],
                                          }})

### ASYNC MESSAGES ###
def send_gesco_new_products(products):
    #print("Sending to gesco")
    products["functionname"] = "catalogue-add-product"
    to =  "gestion-commerciale"
    time = api.send_request('scheduler', 'clock/time')
    message = { "from" : os.environ['DJANGO_APP_NAME'], "to" : to, "datetime" : time, "body" : products}
    queue.send(to, json.dumps(message, cls=DjangoJSONEncoder))
    return

### ASYNC FILES ###
@csrf_exempt
def testfile(request):
    req_data = (request.POST)
    #print(req_data)
    return HttpResponse(200)

def register(request):
    r = requests.post('http://127.0.0.1:5001/register', data={'app': 'catalogue-produit',
                                                              'path': '/mnt/technical_base/catalogue-produit/tests',
                                                              'route': 'http://127.0.0.1:9070/testfile'})
    return HttpResponse(r)

def unregister(request):
    r = requests.post('http://127.0.0.1:5001/unregister', data={'app': 'catalogue-produit'})
    return HttpResponse(r)

def write_catalogue_to_file(request):
    return send_catalogue_file('catalogue-produit')

def send_catalogue_file(destination_app):
    with open(os.path.join(os.getcwd(), "catalogue.json"), "w+") as f:
        produits = Produit.objects
        if destination_app == "ecommerce":
            produits = produits.exclude(exclusivite__exact="magasin")
        elif destination_app == "magasin":
            produits = produits.exclude(exclusivite__exact="ecommerce")
        else:
            produits = produits.all()
        json_data = list(produits.values())
        json_data = {"produits" : json_data}
        f.write(json.dumps(json_data, cls=DjangoJSONEncoder))
    ## Send the catalogue to the app
    r = requests.post('http://127.0.0.1:5001/send', data={'me': os.environ['DJANGO_APP_NAME'],
                                                              'app': destination_app,
                                                              'path': os.path.join(os.getcwd(), "catalogue.json"),
                                                              'name_file' : 'catalogue.json'})
    if r.status_code == 200:
        #print("Sent file to %s : %s" % (destination_app, r.text))
        r = requests.post('http://127.0.0.1:5001/manage')
    #else:
        #print("Error when sending file to %s : %s" % (destination_app, r.text))
    return HttpResponse(r.text)     

### SIMULATEUR ###
@csrf_exempt
def load_from_fournisseur(request):
    status_code, response = api.get_request('fo', 'products')
    if status_code != 200:
        return JsonResponse({"error" : response.text})
    code, response2 = api.post_request2('catalogue-produit', 'load-data', json.dumps(response.json()))
    if code != 200:
        return JsonResponse({"error" : response.text})
    return JsonResponse({ "response" : response2.json() })


### FILTERS ###
def filter(query_set, familleProduit):
    if (familleProduit):
        query_set = query_set.filter(familleProduit__exact=familleProduit)
    return query_set

### HELPERS ###
def my_update_or_create(codeProduit, defaults, unchanged):
    try:
        produit = Produit.objects.get(codeProduit=codeProduit)
        for key, value in defaults.items():
            setattr(produit, key, value)
        produit.save()
        return produit, False
    except Produit.DoesNotExist:
        new_values = {'codeProduit': codeProduit}
        new_values.update(defaults)
        new_values.update(unchanged)
        produit = Produit(**new_values)
        produit.save()
        return produit, True