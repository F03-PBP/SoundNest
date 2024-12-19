from django.urls import path
from django.contrib.auth import views as auth_views

from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('login/', user_login, name='login_page'),
    path('register/', user_register, name='register_page'),
    path('logout/', user_logout, name='logout'),
    path('flutter/login/', flutter_login, name='flutter_login'),
    path('flutter/register/', flutter_register, name='flutter_register'),
    path('flutter/logout/', flutter_logout, name='flutter_logout'),
]
