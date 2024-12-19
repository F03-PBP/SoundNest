from django.urls import path
from reviews.views import *

app_name = 'reviews'

urlpatterns = [
    path('show_reviews', show_reviews, name='show_reviews'),
    path('add/', add_review, name='add_review'),
    path('edit/<uuid:review_id>/', edit_review, name='edit_review'),
    path('delete/<uuid:review_id>/', delete_review, name='delete_review'),
    path('api/', review_list, name='review_list'),
    path('flutter/show_reviews/<str:product_id>/', show_reviews_flutter, name='show_reviews_flutter'),
]
