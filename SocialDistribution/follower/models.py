from django.db import models
from SocialDistribution.authors.models import Author


# Create your models here.
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