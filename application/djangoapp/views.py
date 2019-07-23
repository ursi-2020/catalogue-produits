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
    ventes = Vente.objects.all()
    articles = Article.objects.all()
    context = {'ventes': ventes, 'articles' : articles}
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
    ventes = serializers.serialize("json", Vente.objects.all())
    articles = serializers.serialize("json", Article.objects.all())
    return JsonResponse({'ventes' : ventes, 'articles' : articles})