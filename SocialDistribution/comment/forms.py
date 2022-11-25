from django import forms
from comment.models import *

# comment form
class CommentForm(forms.Form):
    content_type = (("text/markdown", "text/markdown"),
                    ("text/plain", "text/plain"),
                    )
    contentType = forms.CharField(max_length=20, required=True, widget=forms.Select(choices=content_type))
    text = forms.CharField(required=False)
    file = forms.FileField(required=False)
    
    fields = [
        'content_type',
        'text'
        'file'
    ]
    

    