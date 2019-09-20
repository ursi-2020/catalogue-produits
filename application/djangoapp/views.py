from django.http import HttpResponseRedirect
from apipkg import api_manager as api
from application.djangoapp.models import *
from django.shortcuts import render
from .forms import ArticleForm, UserForm
from django.http import JsonResponse
<<<<<<< HEAD
from django.core import serializers
=======
from .models import Article
from django.views.decorators.csrf import csrf_exempt
>>>>>>> 07add1244bcfa8c555c5019f735b35264998aa18
import json


def index(request):
    context = {}
    return render(request, 'index.html', context)

def info(request):
    articles = Article.objects.all()
    context = {'articles' : articles}
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

def load_data(request):
    json_file = open('/static/data.json')

    json_data = json.load(json_file)

    print(json_data)
    json_file.close()

    return HttpResponse("OK")

def api_info(request):
    data = api.send_request('gestion-commercial', 'api-info')
    context = json.loads(data)
    return render(request, 'info_gestion_commerciale.html', context)


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
