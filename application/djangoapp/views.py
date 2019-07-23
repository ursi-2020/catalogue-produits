from django.http import HttpResponse
from django.http import HttpResponseRedirect
from apipkg import api_manager as api
from application.djangoapp.models import *
from django.shortcuts import render
from .forms import ArticleForm
from django.http import JsonResponse
from django.core import serializers


def index(request):
    context = {}
    return render(request, 'index.html', context)

def info(request):
    articles = Article.objects.all()
    context = {'articles' : articles}
    return render(request, 'info.html', context)

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
    articles = serializers.serialize("json", Article.objects.all())
    return JsonResponse({'articles' : articles})

def info_gestion_commerciale(request):
    context = api.send_request('gestioncommerciale', 'api/info')
    return render(request, 'info_gestion_commerciale.html', context)