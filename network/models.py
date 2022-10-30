from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_('The Email must be set'))
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
    
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20,unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Author(models.Model):
    username =models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="profile")
    type = models.CharField(default="author", max_length=200)
    userId = models.UUIDField(unique=True, default=uuid.uuid4, editable=True)
    url = models.CharField(max_length=200)
    host = models.CharField(max_length=200)
    displayName = models.CharField(max_length=200, null=True, blank=True)
    github = models.CharField(max_length=200, null=True, blank=True)
    profileImage = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.displayName

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
    savers = models.ManyToManyField(Author,blank=True , related_name='saved')
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
            "commenter": self.commenter.serialize(),
            "body": self.comment_content,
            "timestamp": self.comment_time.strftime("%b %d %Y, %I:%M %p")
        }
    
class Follower(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='followers')
    followers = models.ManyToManyField(Author, blank=True, related_name='following')

    def __str__(self):
        return f"User: {self.user}"
        