from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
import uuid
from django.db.models import DateTimeField
from django.contrib.auth.models import User

class Author(models.Model):
    username = models.CharField(unique=True, max_length=200, primary_key=True)
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


class Follower(models.Model):
    type = models.CharField(default='followers', max_length=200)
    user = models.OneToOneField(Author, on_delete=models.CASCADE) #related_name = "username")
    items = models.ManyToManyField(Author, related_name='items', blank=True)

    def __str__(self):
        return self.user.username

    def to_dict(self):
        return {
            'type': self.type,
            'items': self.items,
        }

class FollowRequest(models.Model):
    type = models.CharField(default='Follow', max_length=200)
    summary = models.TextField()
    actor = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='%(class)s_request_sender')
    object = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='%(class)s_request_receiver')
    # see https://stackoverflow.com/questions/22538563/django-reverse-accessors-for-foreign-keys-clashing

    def __str__(self):
        return self.actor.username

    def to_dict(self):
        return {
            'type': self.type,
            'summary': f'{self.actor.displayName} wants to follow {self.object.displayName}',
            'actor': self.actor.username,
            'object': self.object.username,
        }
 
class POST(models.Model): 

    CONTENT_TYPE = (
        ('text/markdown', 'text/markdown'),
        ('text/plain','text/plain'),
        ('application/base64', 'application/base64'),
        ('image/png;base64','image/png;base64'),
        ('image/jpeg;base64','image/jpeg;base64')
    )

    VISIBILITY_CHOICES = (
        ('PUBLIC','PUBLIC'),
        ("FRIENDS","FRIENDS")
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    source = models.URLField(null=True, blank=True)
    origin = models.URLField(null=True, blank=True)
    content = models.CharField(max_length=500, blank=True, null=True)
    contentType = models.CharField(max_length=255, choices=CONTENT_TYPE, default='text/plain')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    image_url = models.URLField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    comment_count = models.IntegerField(default=0)
    published = models.DateTimeField(auto_now=True)
    visibility = models.CharField(max_length=15, choices=VISIBILITY_CHOICES, default="PUBLIC")
    unlisted = models.BooleanField(default=False)


    class Meta:
        ordering = ['-published']

    def __str__(self):
        return self.title

    @property
    def type(self):
        return 'post'