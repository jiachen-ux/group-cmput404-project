from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
import uuid
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone


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
        other.setdefault('is_active', True)
        other.setdefault('is_staff', True)
        other.setdefault('is_superuser', True)
  
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

class Post(models.Model):
    creater = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    date_created = models.DateTimeField(default=timezone.now)
    content_text = models.TextField(max_length=140, blank=True)
    content_image = models.ImageField(upload_to='posts/', blank=True)
    likers = models.ManyToManyField(Author,blank=True , related_name='likes')
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Post user: {self.id} (creater: {self.creater})"

    def img_url(self):
        return self.content_image.url

    def append(self, name, value):
        self.name = value

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='commenters')
    comment_content = models.TextField(max_length=90)
    comment_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Post: {self.post} | Commenter: {self.commenter}"

    def to_dict(self):
        return {
            "id": self.id,
            "commenter": self.commenter.to_dict(),
            "body": self.comment_content,
            "timestamp": self.comment_time.strftime("%b %d %Y, %I:%M %p")
        }
    
class Follower(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='followers')
    followers = models.ManyToManyField(Author, blank=True, related_name='following')

    def __str__(self):
        return f"User: {self.user}"

