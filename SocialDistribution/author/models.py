from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
import uuid
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone


class AuthorManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError('Users must have an username')
        
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password, **other):
        other.setdefault('is_superuser', True)
        other.setdefault('is_staff', True)
        other.setdefault('is_active', True)
        return self.create_user(username, password,**other)

     


class Author(AbstractBaseUser,PermissionsMixin ):

    username= models.CharField(unique=True, max_length=200)
    type = models.CharField(default="author", max_length=200)
    userid = models.UUIDField(default=uuid.uuid4, editable=True)
    url = models.CharField(max_length=200, blank=True)
    host = models.CharField(max_length=200, blank=True)
    displayName = models.CharField(max_length=200, null=True, blank=True)
    github = models.CharField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(blank=True)
    is_active=  models.BooleanField(default=True)
    is_staff=  models.BooleanField(default=True)
    is_superuser=  models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = AuthorManager()

    def __str__(self):
        return self.username

    def to_dict(self):
        return {
            'type': self.type,
            'username':self.username,
            'id': self.userid,
            'url': self.url,
            'host': self.host,
            'displayName': self.displayName,
            'github': self.github
        }
    def usern(self):
        return self.username