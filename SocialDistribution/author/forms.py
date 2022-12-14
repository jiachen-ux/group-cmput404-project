from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db.models.fields import CharField
from rest_framework.fields import EmailField
from .models import AuthorUserManager, Author

class CreateAuthorForm(UserCreationForm):
    class Meta:
        model = Author
        fields = ['displayName','username', 'password1', 'password2', 'github']

    displayName= forms.CharField(max_length=100,
                           widget= forms.TextInput
                           (attrs={'class':'form-control'}))

    username= forms.CharField(max_length=100,
                           widget= forms.TextInput
                           (attrs={'class':'form-control'}))

    password1 = forms.CharField(max_length=100,
                           widget= forms.PasswordInput
                           (attrs={'class':'form-control'}))

    password2 = forms.CharField(max_length=100,
                           widget= forms.PasswordInput
                           (attrs={'class':'form-control'}))

    github = forms.CharField(max_length=100,
                           widget= forms.TextInput
                           (attrs={'class':'form-control'}))


class EditAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('displayName', 'username', 'github')