from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Author


# Create your forms here.

class UserRegisterForm(UserCreationForm):
	class Meta:
		model = Author
		fields = ("username", "github", "password1", "password2")

	def save(self, commit=True):
		user = super(UserRegisterForm, self).save(commit=False)
		if commit:
			user.save()
		return user