from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
import uuid
from django.contrib.auth.models import PermissionsMixin


class AuthorManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('Users must have an email address')
        
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password, **other):
        other.setdefault('is_active', 'True')
        other.setdefault('is_staff', 'True')
        other.setdefault('is_superuser', 'True')
  
        return self.create_user(username, password,
         **other)

     


class Author(AbstractBaseUser,PermissionsMixin ):
    username = models.CharField(unique=True, max_length=200, primary_key=True)
    type = models.CharField(default="author", max_length=200)
    userId = models.UUIDField(unique=True, default=uuid.uuid4, editable=True)
    url = models.CharField(max_length=200)
    host = models.CharField(max_length=200)
    displayName = models.CharField(max_length=200, null=True, blank=True)
    github = models.CharField(max_length=200, null=True, blank=True)
    profileImage = models.CharField(max_length=500, null=True, blank=True)
    is_active=  models.BooleanField(default=False)
    is_staff=  models.BooleanField(default=False)
    is_superuser=  models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = AuthorManager()

    def __str__(self):
        return self.username

    def to_dict(self):
        return {
            'type': self.type,
            'id': self.userId,
            'url': self.url,
            'host': self.host,
            'displayName': self.displayName,
            'github': self.github,
            'profileImage': self.profileImage,
        }