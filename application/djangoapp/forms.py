from django.forms import ModelForm
from .models import Article, User
class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['nom', 'stock']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['nom', 'prenom', 'age']