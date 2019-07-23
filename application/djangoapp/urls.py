from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info', views.info, name='info'),
    path('info-gestion-commerciale', views.info_gestion_commerciale, name='info-gestion-commerciale'),
    path('api-info', views.api_info, name='api-info'),
    path('api-add-article', views.api_add_article, name='api-add-article'),
    path('add-article', views.add_article, name='add-article'),
    path('add-user-gestion-commerciale', views.add_user_gestion_commerciale, name='add-user-gestion-commerciale'),
]