from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from uuid import uuid4
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from email.policy import default

from SocialDistribution.settings import HOSTNAME


def post_upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)

def profile_upload_to(instance, filename):
    return 'profile/{filename}'.format(filename=filename)

class AuthorUserManager(BaseUserManager):
    def create_user(self, username, password=None, displayName=None, github=None, **other_fields):
       
        if not username:
            raise ValueError('username must not be empty')
        
        if not password:
            raise ValueError('password must not be empty')
        user = self.model(username=username, displayName=displayName, github=github, **other_fields)
        user.set_password(password)
        user.save()
        return user
 
    def create_superuser(self, username, password=None, **other_fields):
        other_fields.setdefault('is_active', 'True')
        other_fields.setdefault('is_staff', 'True')
        other_fields.setdefault('is_superuser', 'True')

        return self.create_user(username, password, **other_fields)


class Author(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    join_date = models.DateTimeField(auto_now_add=True)
    profileImage = models.ImageField(upload_to = profile_upload_to, null=True, blank=True)
    host = models.CharField(max_length=255, blank=True, default=HOSTNAME)
    url = models.URLField(max_length=255, blank=True)
    github = models.URLField(max_length=255, blank=True, null=True)
    displayName = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    @property
    def type(self):
        return 'author' 

    def url(self):
        return self.host + "authors/" + str(self.id)

    objects = AuthorUserManager()

