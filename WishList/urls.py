from django.urls import path
from WishList.views import *


app_name = 'main'


urlpatterns = [
    path('', view_wishlist, name='guest_page'),
    path('produk/', get_produk_list, name='get_produk_list'),
    path('delete/<uuid:id>', delete_wish, name='delete_wish'), 
    #path('home/', home, name='home'),
    #path('login/', login_user, name='login'),
    #path('register/', register_user, name='register'),
    #path('logout/', logout_user, name='logout'),
]