from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
import uuid
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from SocialDistribution.settings import HOSTNAME




class AuthorManager(BaseUserManager):
    def create_user(self, username, password=None,displayName=None, github=None, **other_fields):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError('Users must have an username')
        
        user = self.model(username=username,displayName=displayName, github=github, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **other_fields):
        other_fields.setdefault('is_active', 'True')
        other_fields.setdefault('is_staff', 'True')
        other_fields.setdefault('is_superuser', 'True')
    
        return self.create_user(username, password,**other_fields)

     


class Author(AbstractBaseUser,PermissionsMixin ):
    username= models.CharField(unique=True, max_length=200)
    joined_date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(default="author", max_length=200)
    userid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.CharField(max_length=200, blank=True)
    host = models.CharField(max_length=255, blank=True, default=HOSTNAME)
    displayName = models.CharField(max_length=200, null=True, blank=True)
    github = models.CharField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(blank=True)
    is_active=  models.BooleanField(default=True)
    is_staff=  models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = AuthorManager()

    def __str__(self):
        return self.username

    def to_dict(self):
        return {
            'username':self.username,
            'type':self.type,
            'joined_date':self.joined_date,#
            'userid': self.userid,
            'url': self.host + "authors/" + str(self.userid),#
            'host': self.host,
            'displayName': self.displayName,
            'github': self.github
        } 
    def url(self):
        return self.host + "authors/" + str(self.userid)
    
