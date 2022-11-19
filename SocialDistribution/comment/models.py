from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from uuid import uuid4
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from email.policy import default
from SocialDistribution.settings import HOSTNAME
from author.models import Author
from post.models import POST

# Create your models here.
class Comment(models.Model):
    CONTENT_TYPE = (
        ('text/markdown', 'text/markdown'),
        ('text/plain','text/plain')
    )

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(POST, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    published = models.DateTimeField(auto_now_add=True)
    contentType = models.CharField(max_length=255, choices=CONTENT_TYPE, default='text/markdown')
 
    class Meta:
        ordering = ['-published']
    
    def __str__(self):
        return self.author.username + '/' + self.post.title
         
    @property
    def type(self):
        return 'comment'
    
    def get_id(self):
        return self.post.origin + "authors/" + str(self.author.id) + "/posts/" + str(self.post.id) + "/comments/" + str(self.id)