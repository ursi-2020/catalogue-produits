
from django.forms import ModelForm
from django import forms
from .models import Article
class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['nom', 'stock']