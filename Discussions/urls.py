from django.urls import path
from . import views

urlpatterns = [
    path('create_thread/', views.create_thread, name='create_thread'),
    path('add_comment/<int:thread_id>/', views.add_comment, name='add_comment'),
    path('view_threads/', views.view_threads, name='view_threads'),
]
