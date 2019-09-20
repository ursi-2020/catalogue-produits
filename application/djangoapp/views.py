from django.http import HttpResponseRedirect
from django.http import HttpResponse
from apipkg import api_manager as api
from application.djangoapp.models import *
from django.shortcuts import render
from .forms import ArticleForm, UserForm
from django.http import JsonResponse
from django.core import serializers
from .models import Article
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json

def index(request):
    if request.method == 'POST' and request.FILES['file']:
        json_data = json.loads(request.FILES['file'].read())
        load_data(json_data)
        return HttpResponseRedirect('/catalogueproduit/info')
    else:
        return render(request, 'index.html', {})


def info(request):
    produits = Produit.objects.all()
    context = {'produits' : produits}
    return render(request, 'info.html', context)

@csrf_exempt
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            new_article = form.save()
            return HttpResponseRedirect('/info')
    else:
        form = ArticleForm()
    return render(request, 'add_article.html', {'form' : form})

def api_info(request):
    articles = list(Article.objects.all().values())
    return JsonResponse({'articles' : articles})

@csrf_exempt
def api_add_article(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        print(body)
        new_user = Article(nom=body["nom"], stock=body["stock"])
        new_user.save()
        return HttpResponseRedirect('/info')
    return HttpResponse("OK")



def info_gestion_commerciale(request):
    context = api.send_request('gestioncommerciale', 'api/info')
    return render(request, 'info_gestion_commerciale.html', context)


def load_data(json_data):
    for product in json_data["produits"]:
        new_product = Produit(codeProduit=product["codeProduit"], familleProduit=product["familleProduit"], descriptionProduit=product["descriptionProduit"], quantiteMin=product["quantiteMin"], packaging=product["packaging"], prix=product["prix"])
        new_product.save()
    return HttpResponse(json.dumps(json_data))

def api_data(request):
    id = request.GET.get('id')
    if (id):
        # If one article is specified, try to retrieve this one
        try:
            produit = Produit.objects.get(id=id)
        except Produit.DoesNotExist:
            return JsonResponse({'error': 'Code produit invalide ou produit inexistant'}, status=404)
        else:
            return JsonResponse({'produit' : model_to_dict(produit)})
    else:
        # If no id is specified, return every product
        produits = list(Produit.objects.all().values())
        return JsonResponse({'produits' : produits})

#def api_info(request):
 #   data = api.send_request('gestion-commercial', 'api-info')
  #  context = json.loads(data)
   # return render(request, 'info_gestion_commerciale.html', context)


def add_user_gestion_commerciale(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            dump = json.dumps(clean_data)
            sent = api.post_request('gestion-commercial', 'api-add-user', dump)
    else:
        form = UserForm()
    return render(request, 'add_user.html', {'form': form})
