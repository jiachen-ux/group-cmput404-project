from django.db import models
from author.models import Author
from uuid import uuid4
from django.utils import timezone

# Create your models here.
class Comment(models.Model):
    type = models.CharField(blank=False, null=False, default="comment", max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    id = models.URLField(blank=True, null=False)
    comment = models.TextField(max_length=90)
    contentType = models.CharField(default='text/markdown', blank=False, null=False, max_length=200)
    published = models.DateTimeField(default=timezone.now)

    # def __str__(self):
    #     return f"Post: {self.post} | Commenter: {self.commenter}"

    def to_dict(self):
        return {
            "id": self.id,
            "commenter": self.commenter.to_dict(),
            "body": self.comment_content,
            "timestamp": self.comment_time.strftime("%b %d %Y, %I:%M %p")
        }

class CommentSrc(models.Model):
    type = models.CharField(blank=False, null=False, default="comments", max_length=200)
    page = models.PositiveIntegerField(default=1)
    size = models.PositiveIntegerField(default=5)
    post = models.URLField(blank=True, null=False)
    uuid = models.UUIDField(default=uuid4, editable=False)
    id = models.URLField(primary_key=True, blank=True, null=False)
    comments = models.ManyToManyField(Comment, blank=True)