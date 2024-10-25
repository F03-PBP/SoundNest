from django.contrib import admin
from django.urls import path, include

app_name = 'Discussions'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Discussions.urls')),
]
