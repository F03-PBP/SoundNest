from django import forms
from .models import DiscussionThread, DiscussionComment

class DiscussionThreadForm(forms.ModelForm):
    class Meta:
        model = DiscussionThread
        fields = ['title', 'content']

class DiscussionCommentForm(forms.ModelForm):
    class Meta:
        model = DiscussionComment
        fields = ['content']
