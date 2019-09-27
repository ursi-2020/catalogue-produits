from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info', views.info, name='info'),
    path('load-data', views.load_data, name='load-data'),
    path('schedule-load-data', views.schedule_load_data, name='schedule-load-data'),
    path('automatic-load-data', views.automatic_load_data, name='automatic-load-data'),
    path('clear-data', views.clear_data, name='clear-data'),
    path('api/data', views.api_data, name='api-data'),
]