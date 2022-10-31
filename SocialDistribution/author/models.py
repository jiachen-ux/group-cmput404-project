from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
import uuid
from django.contrib.auth.models import PermissionsMixin

# Create your models here.
class AuthorManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):

        if not username:
            raise ValueError('Users must have an useraname')
        
        user = self.model(username=username, **kwargs)
     
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password, **other):
        other.setdefault('is_active', True)
        other.setdefault('is_staff', True)
        other.setdefault('is_superuser', True)
  
        return self.create_user(username, password,**other)

     


class Author(AbstractBaseUser,PermissionsMixin):

    username= models.CharField(unique=True, max_length=200)
    type = models.CharField(default="author", max_length=200, null=False)
    userid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=True)
    url = models.URLField(max_length=200, blank=True)
    host = models.CharField(max_length=200, blank=True)
    displayName = models.CharField(max_length=200, null=True, blank=True)
    github = models.URLField(max_length=200, null=True, blank=True)
    profileImage = models.URLField(blank=True)
    is_active=  models.BooleanField(default=True)
    is_staff=  models.BooleanField(default=False)
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
            'github': self.github,
            'profileImage': self.profileImage
        }