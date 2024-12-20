from django.urls import path
from .views import create_thread, add_comment, view_threads

app_name = 'Discussions'

urlpatterns = [
    path('create_thread/', create_thread, name='create_thread'),
    path('add_comment/<int:thread_id>/', add_comment, name='add_comment'),
    path('view_threads/', view_threads, name='view_threads'),
]
