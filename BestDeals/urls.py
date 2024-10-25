from django.urls import path
from .views import best_deals, delete_product, add_to_deals_ajax  # Import the view

urlpatterns = [
    path('', best_deals, name='best_deals'),  # URL for best deals
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
    path('add-to-deals/', add_to_deals_ajax, name='add_to_deals_ajax'),
]
