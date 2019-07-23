from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info', views.info, name='info'),
    path('api/info', views.api_info, name='api-info'),
    path('add-article', views.add_article, name='add-article'),
]