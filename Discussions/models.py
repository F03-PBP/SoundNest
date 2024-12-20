from django.db import models

class DiscussionThread(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    product_id = models.IntegerField(null=True, blank=True) 

    def __str__(self):
        return self.title

class DiscussionComment(models.Model):
    thread = models.ForeignKey(DiscussionThread, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment on {self.thread.title}'

# Create your models here.

