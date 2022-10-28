from django.db import models
import uuid
from django.db.models import DateTimeField
from authors.models import Author
# Create your models here.
class Post(models.Model):
    CONTENT_TYPES = [
        ("text/markdown", "text/markdown"),
        ("text/plain", "text/plain"),
        ("application/base64","application/base64"),
        ("image/png;base64","image/png;base64"),
        ("image/jpeg;base64","image/jpeg;base64")
    ]
    VISIBILITY = [
        ("PUBLIC", "PUBLIC"),
        ("FRIENDS", "FRIENDS"),
        ("PRIVATE", "PRIVATE")
    ]
    type = models.CharField(max_length=4, default="post", editable=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    content_type = models.CharField(max_length=30, choices = CONTENT_TYPES, default="text/plain")
    content = models.TextField(blank=True, null=True)
    visibility = models.CharField(max_length=30, choices = VISIBILITY, default="PUBLIC")
    unlisted = models.BooleanField(default=False)
    published = DateTimeField('date published', auto_now_add=True, editable=False)
    source = models.URLField(blank=True)
    origin = models.URLField(blank=True)
    author = models.ForeignKey(Author, blank=False, null=False, on_delete=models.CASCADE)
    description = models.CharField(max_length=240, blank=True, null=True, default="")
    edited_at = models.DateTimeField("date edited",auto_now=True)

    class Meta:
        ordering = ('-published',)

    def __str__(self) -> str:
        return self.title + " (" + str(self.id) + ")"