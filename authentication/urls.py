from django.urls import path
from django.contrib.auth import views as auth_views

from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login_page'),
    path('register/', user_register, name='register_page'),
    path('logout/', user_logout, name='logout'),
]
