# Discussions/views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import DiscussionThread, DiscussionComment
from .forms import DiscussionThreadForm, DiscussionCommentForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Handle CSRF appropriately in production
def create_thread(request):
    if request.method == 'POST':
        form = DiscussionThreadForm(request.POST)
        print("Received data:", request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.product_id = request.POST.get('product_id', None)
            thread.save()
            return JsonResponse({
                'id': thread.id,
                'title': thread.title,
                'content': thread.content,
                'created_at': thread.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }, status=201)
        else:
            print("Form errors:", form.errors)
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = DiscussionThreadForm()
    return render(request, 'create_thread.html', {'form': form})

@csrf_exempt  # Handle CSRF appropriately in production
def add_comment(request, thread_id):
    thread = get_object_or_404(DiscussionThread, id=thread_id)
   
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = DiscussionCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.save()
            return JsonResponse({
                'id': comment.id,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
   
    else:
        form = DiscussionCommentForm()
   
    return render(request, 'add_comment.html', {'form': form, 'thread': thread})

def view_threads(request):
    threads = DiscussionThread.objects.all().order_by('-created_at')
    threads_data = []
    for thread in threads:
        comments = thread.comments.all().order_by('created_at')
        comments_data = [
            {
                'id': comment.id,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for comment in comments
        ]
        threads_data.append({
            'id': thread.id,
            'title': thread.title,
            'content': thread.content,
            'created_at': thread.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'product_id': thread.product_id,
            'comments': comments_data,
        })
    return JsonResponse({'threads': threads_data}, status=200)
