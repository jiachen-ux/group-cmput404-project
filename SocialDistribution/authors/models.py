from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
import uuid

class Author(models.Model):
    username = models.CharField(unique=True, max_length=200, primary_key=True)
    type = models.CharField(default="author", max_length=200)
    userId = models.UUIDField(unique=True, default=uuid.uuid4, editable=True)
    url = models.CharField(max_length=200)
    host = models.CharField(max_length=200)
    displayName = models.CharField(max_length=200, null=True)
    github = models.CharField(max_length=200, null=True)
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