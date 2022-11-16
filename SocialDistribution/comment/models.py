from django.db import models
from author.models import Author
from uuid import uuid4
from django.utils import timezone
import uuid
from uuid import uuid4
from post.models import Post

# Create your models here.
class Comment(models.Model):
    commentid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='commenters')
    comment_content = models.TextField(max_length=90)
    comment_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Post: {self.post} | Commenter: {self.commenter}"

    def to_dict(self):
        return {
            "id": self.commentid,
            "commenter": self.commenter.to_dict(),
            "body": self.comment_content,
            "timestamp": self.comment_time.strftime("%b %d %Y, %I:%M %p")
        }