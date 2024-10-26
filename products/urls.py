from django.urls import path
from products.views import *

app_name = 'products'

urlpatterns = [
    path('api/products/', get_products, name='get_products'),
    path('', show_product, name='show_products'),
]