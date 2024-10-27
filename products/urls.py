from django.urls import path
from products.views import *

app_name = 'products'

urlpatterns = [
    path('api/products/', get_products, name='get_products'),
    path('', show_product, name='home'),
    path('details/<uuid:product_id>/', product_details, name='product_details'),
    path('add_product/', add_product, name='add_product'),
    path('delete_product/', delete_product, name='delete_product'), 
    path('details/json/<uuid:product_id>/', product_details_json, name='product_details_json'),
    path('edit_product', edit_product, name='edit_product'),
]