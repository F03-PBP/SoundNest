from django.urls import path
from WishList.views import *


app_name = 'WishList'


urlpatterns = [
    path('view_wishlist', view_wishlist, name='view_wishlist'),
    path('json/product', get_product_json, name='get_product_json'),
    path('json/wishlist', get_wishlist_json, name='get_wishlist_json'),
    path('json/<str:id>/', get_product_json_by_id, name='get_product_json_by_id'),
    path('add-product-entry-ajax', add_product_entry_ajax, name='add_product_entry_ajax'),
    path('delete/<int:id>/', delete_wish, name='delete_wish'),
    path('create-wishlist-flutter/', create_wishlist_flutter, name='create_wishlist_flutter'),
    path('delete_flutter/', delete_flutter, name='delete_flutter'),
    path('edit_quantity_flutter/', edit_quantity_flutter, name='edit_quantity_flutter'),
    #path('home/', home, name='home'),
    #path('login/', login_user, name='login'),
    #path('register/', register_user, name='register'),
    #path('logout/', logout_user, name='logout'),
]