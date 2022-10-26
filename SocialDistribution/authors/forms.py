from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(UserRegisterForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

from django.conf import settings
from tkinter.tix import TCL_WINDOW_EVENTS
from django import forms
from .models import POST
 

class PostForm(forms.ModelForm):

    class Meta:
        model = POST
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get("content")
        # if len(content) > max_post_length:
        #     raise forms.ValidationError("This post is too long")
        return content
