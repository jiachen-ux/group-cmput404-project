from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from uuid import uuid4
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from email.policy import default
from SocialDistribution.settings import HOSTNAME
from author.models import Author



# Create your models here.

class Follower(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    #sender
    follower = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='follower')
    #recevier
    following = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='following')
    # timestamp
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def type(self):
        return 'friend'


class FollowRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    sender = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='receiver')
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def type(self):
        return 'follow'

