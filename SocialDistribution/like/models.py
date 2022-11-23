from django.db import models
from uuid import uuid4
from author.models import Author
from comment.models import Comment
from post.models import Post

# Create your models here.
class Like(models.Model):

    TYPE_CHOICES = (
        ('post','post'),
        ("comment","comment")
    )

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    object_type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True)
    object_id = models.URLField(null=True) 
    published = models.DateTimeField(auto_now_add=True)

    @property
    def type(self):
        return 'Like'

    def summary(self):
        return self.author.displayName + " Likes your " + self.object_type

    def object_url(self):
        if self.object_type == "post":
            return Post.objects.get(id=self.object_id).get_id()
        elif self.object_type == "comment":
            return Comment.objects.get(id=self.object_id).get_id()