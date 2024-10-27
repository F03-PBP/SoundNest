from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import DiscussionThread, DiscussionComment
from .forms import DiscussionThreadForm, DiscussionCommentForm

# Create your views here.

def create_thread(request):
    if request.method == 'POST':
        form = DiscussionThreadForm(request.POST)
        if form.is_valid():
            thread = form.save()
            return JsonResponse({'id': thread.id, 'title': thread.title, 'content': thread.content, 'created_at': thread.created_at.strftime('%Y-%m-%d %H:%M:%S')})
    else:
        form = DiscussionThreadForm()
    return render(request, 'Discussions/create_thread.html', {'form': form})

def add_comment(request, thread_id):
    thread = DiscussionThread.objects.get(id=thread_id)
    if request.method == 'POST':
        form = DiscussionCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.save()
            return JsonResponse({'content': comment.content, 'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')})
    else:
        form = DiscussionCommentForm()
    return render(request, 'Discussions/add_comment.html', {'form': form, 'thread': thread})

def view_threads(request):
    threads = DiscussionThread.objects.all()
    return render(request, 'Discussions/view_threads.html', {'threads': threads})
