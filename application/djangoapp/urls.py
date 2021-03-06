from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info', views.info, name='info'),
    path('load-data', views.load_data, name='load-data'),
    path('schedule-load-data', views.schedule_load_data, name='schedule-load-data'),
    path('automatic-load-data', views.automatic_load_data, name='automatic-load-data'),
    path('clear-data', views.clear_data, name='clear-data'),
    path('clear-logs', views.clear_logs, name='clear-logs'),
    ## TESTS ROUTES ##
    path('load-from-fournisseur', views.load_from_fournisseur, name='load-from-fournisseur'),

    ## File manager routes ##
    path('testfile', views.testfile, name='testfile'),
    path('register', views.register, name='register'),
    path('unregister', views.unregister, name='unregister'),

    path('write-to-file', views.write_catalogue_to_file, name='write-to-file'),
    ## API ROUTES ##
    path('api/get-all', views.api_get_all, name='api-get-all'),
    path('api/get-ecommerce', views.api_get_ecommerce, name='api-get-ecommerce'),
    path('api/get-magasin', views.api_get_magasin, name='api-get-magasin'),
    path('api/get-by-id/<str:code_produit>', views.api_get_by_id, name='api-get-by-id'),
    path('api/file/products', views.api_get_products_by_file, name='api-get-products-by-file'),
    path('api/simulateur/get-all-ecommerce', views.api_simulateur_get_all_ecommerce, name='api-simulateur-get-all-ecommerce'),
    path('api/simulateur/get-by-code', views.api_simulateur_get_by_code, name='api-simulateur-get-by-code')
]
