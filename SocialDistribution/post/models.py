from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from uuid import uuid4
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from email.policy import default
from SocialDistribution.settings import HOSTNAME
from author.models import Author

def post_upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)

def profile_upload_to(instance, filename):
    return 'profile/{filename}'.format(filename=filename)

class Post(models.Model): 

    CONTENT_TYPE = (
        ('text/markdown', 'text/markdown'),
        ('text/plain','text/plain'),
        ('application/base64', 'application/base64'),
        ('image/png;base64','image/png;base64'),
        ('image/jpeg;base64','image/jpeg;base64')
    )

    VISIBILITY_CHOICES = (
        ("PUBLIC","PUBLIC"),
        ("FRIENDS","FRIENDS")
    )

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True, default='No Title')
    source = models.URLField(null=True, blank=True, default=HOSTNAME)
    origin = models.URLField(default=HOSTNAME)
    description = models.CharField(max_length=500, blank=True, null=True)
    contentType = models.CharField(max_length=255, choices=CONTENT_TYPE, default='text/plain')
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.TextField(default='[]', null=True)
    image_url = models.URLField(null=True, blank=True)
    #upload_to is a function
    image = models.ImageField(upload_to=post_upload_to, null=True, blank=True)
    count = models.IntegerField(default=0)
    published = models.DateTimeField(auto_now=True)
    visibility = models.CharField(max_length=15, choices=VISIBILITY_CHOICES, default="PUBLIC")
    unlisted = models.BooleanField(default=False)
    url = models.URLField(max_length=500, blank=True)
    comments = models.URLField(max_length=500,editable=False,default=str(url) + '/comments')

    def get_id(self):
        return self.origin + "authors/" + str(self.author.id) + "/posts/" + str(self.id)

    def get_source(self):
        source = str(self.source) if self.source is not None else HOSTNAME
        return source + "posts/" + str(self.id)

    def get_origin(self):
        return str(self.origin) + "posts/" + str(self.id)

    def get_url(self):
        return self.origin + "service/authors/" + str(self.author.id) + "/posts/" + str(self.id)

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return self.title

    @property
    def type(self):
        return 'post'

# from comment.models import Comment

class Inbox(models.Model):

    TYPE_CHOICES = (
        ('post','post'),
        ("comment","comment"),
        ('like','like'),
        ("follow","follow")
    )

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    object_type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True )
    object_id = models.UUIDField(null=True)
    published = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=500, default="No message")

    class Meta:
        ordering = ['-published']
