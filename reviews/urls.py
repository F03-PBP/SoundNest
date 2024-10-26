from django.urls import path
from .views import *

app_name = 'reviews'

urlpatterns = [
    path('', show_reviews, name='rating'),
    path('reviews/', review_list, name='reviews'),
]
