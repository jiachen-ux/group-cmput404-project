import imp
from django.db import models

# Create your models here.
from author.models import Author

class Follower(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='followers')
    followers = models.ManyToManyField(Author, blank=True, related_name='following')

    def __str__(self):
        return f"User: {self.user}"

