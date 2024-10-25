from django.urls import path
from products.views import show_product

app_name = 'products'

urlpatterns = [
    path('', show_product, name='show_product'),
]