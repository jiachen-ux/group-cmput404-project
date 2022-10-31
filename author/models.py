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

class Post(models.Model):
    creater = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    date_created = models.DateTimeField(default=timezone.now)
    content_text = models.TextField(max_length=140, blank=True)
    content_image = models.ImageField(upload_to='posts/', blank=True)
    likers = models.ManyToManyField(Author,blank=True , related_name='likes')
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Post ID: {self.id} (creater: {self.creater})"

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

    def serialize(self):
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
        
    
# class POST(models.Model): 

#     CONTENT_TYPE = (
#         ('text/markdown', 'text/markdown'),
#         ('text/plain','text/plain'),
#         ('application/base64', 'application/base64'),
#         ('image/png;base64','image/png;base64'),
#         ('image/jpeg;base64','image/jpeg;base64')
#     )

#     VISIBILITY_CHOICES = (
#         ('PUBLIC','PUBLIC'),
#         ("FRIENDS","FRIENDS")
#     )

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=255, blank=True, null=True)
#     source = models.URLField(null=True, blank=True)
#     origin = models.URLField(null=True, blank=True)
#     content = models.CharField(max_length=500, blank=True, null=True)
#     contentType = models.CharField(max_length=255, choices=CONTENT_TYPE, default='text/plain')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
#     image_url = models.URLField(null=True, blank=True)
#     image = models.ImageField(null=True, blank=True)
#     comment_count = models.IntegerField(default=0)
#     published = models.DateTimeField(auto_now=True)
#     visibility = models.CharField(max_length=15, choices=VISIBILITY_CHOICES, default="PUBLIC")
#     unlisted = models.BooleanField(default=False)


#     class Meta:
#         ordering = ['-published']

#     def __str__(self):
#         return self.title

#     @property
#     def type(self):
#         return 'post'