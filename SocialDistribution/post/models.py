from django.utils.timezone import now
from django.utils import dateparse
from django.db import models
from author.models import Author
from uuid import uuid4
from django.utils import timezone
from comment.models import CommentSrc, Comment



# Create your models here.
class Post(models.Model):

    CONTENT_TYPE = [("text/plain", "Plaintext"),
                       ("text/markdown", "Markdown"),
                       ("application/base64", "app"),
                       ("image/png;base64", "png"),
                       ("image/jpeg;base64", "jpeg")]
    PUBLIC = 'PUBLIC'
    FRIENDS = 'FRIENDS'

    type = models.CharField(default='post', max_length=200)
    title = models.CharField(max_length=200, blank=True)
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    id = models.URLField(blank=False, null=False)
    source = models.URLField(blank=True)
    origin = models.URLField(blank=True)
    description = models.TextField(null=True, blank=True)
    contentType = models.CharField(max_length=200, blank=False, null=False, choices=CONTENT_TYPE)
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    categories = models.TextField(null=True, blank=True)
    count = models.IntegerField(default=0)
    comments = models.URLField(blank=True)
    commentSrc = models.ForeignKey(CommentSrc, blank=True, null=True, on_delete=models.SET_NULL, related_name = 'commentSrcId')
    published = models.DateTimeField(auto_now_add=True, editable=False)
    visibility = models.CharField(default=PUBLIC, max_length=200)
    unlisted = models.BooleanField(default=False, blank=False, null=False)

    # # def __str__(self):
    # #     return f"Post user: {self.id} (creater: {self.creater})"

    # # def img_url(self):
    # #     return self.content_image.url

    # def append(self, name, value):
    #     self.name = value
