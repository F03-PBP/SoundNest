from django.urls import path
from .views import best_deals, add_to_deals, edit_deals, delete_deals, show_json  # Import the view

urlpatterns = [
    path('', best_deals, name='best_deals'),  # URL for best deals
    path('add-to-deals/', add_to_deals, name='add_to_deals'),
    path('edit-deals/<uuid:product_id>/', edit_deals, name='edit_deals'),
    path('delete-deals/<uuid:product_id>/', delete_deals, name='delete_deals'),
    path('json/', show_json, name='show_json'),
]
