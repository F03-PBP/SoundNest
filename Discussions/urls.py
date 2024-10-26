from django.urls import path
from . import views

app_name = 'Discussions'  # Menambahkan app_name untuk namespace

urlpatterns = [
    path('create_thread/', views.create_thread, name='create_thread'),
    path('add_comment/<int:thread_id>/', views.add_comment, name='add_comment'),
    path('view_threads/', views.view_threads, name='view_threads'),
]
