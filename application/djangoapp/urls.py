from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info', views.info, name='info'),
    path('load-data', views.load_data, name='load-data'),
    path('schedule-load-data', views.schedule_load_data, name='schedule-load-data'),
    path('automatic-load-data', views.automatic_load_data, name='automatic-load-data'),
    path('clear-data', views.clear_data, name='clear-data'),

    ## API ROUTES ##
    path('api/get-all', views.api_get_all, name='api-get-all'),
    path('api/get-ecommerce', views.api_get_ecommerce, name='api-get-ecommerce'),
    path('api/get-magasin', views.api_get_magasin, name='api-get-magasin'),
    path('api/get-by-id/<int:id_product>', views.api_get_by_id, name='api-get-by-id')
]
