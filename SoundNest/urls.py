from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('', include('products.urls')),
    path('reviews/', include('reviews.urls')),
    path('discussion/', include('Discussions.urls')),
]
