from django.conf import settings
from tkinter.tix import TCL_WINDOW_EVENTS
from django import forms
from .models import Post
MAX_POST_LENGTH  = settings.MAX_POST_LENGTH

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > max_post_length:
            raise forms.ValidationError("This post is too long")
        return content
