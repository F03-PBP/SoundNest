from django.urls import path
from django.contrib.auth import views as auth_views

from authentication.views import logout_view

app_name = 'authentication'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
]
