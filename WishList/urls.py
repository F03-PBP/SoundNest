from django.urls import path
from WishList.views import *


app_name = 'WishList'


urlpatterns = [
    path('', view_wishlist, name='guest_page'),
    path('delete/<uuid:id>', delete_wish, name='delete_wish'),
    path('json/', get_product_json, name='get_product_json'), 
    #path('home/', home, name='home'),
    #path('login/', login_user, name='login'),
    #path('register/', register_user, name='register'),
    #path('logout/', logout_user, name='logout'),
]