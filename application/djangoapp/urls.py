from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info', views.info, name='info'),
    path('info-gestion-commerciale', views.info_gestion_commerciale, name='info-gestion-commerciale'),
]