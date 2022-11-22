from django.utils.timezone import now
from django.utils import dateparse
from django.db import models
from author.models import Author
import uuid
from uuid import uuid4
from django.utils import timezone
from SocialDistribution.settings import HOSTNAME


CONTENT = (
        ('text/markdown', 'text/markdown'),
        ('text/plain','text/plain'),
        ('image/png;base64','image/png;base64'),
        ('image/jpeg;base64','image/jpeg;base64')
    )

VISIBILITY= (
    ("PUBLIC","PUBLIC"),
    ("FRIENDS","FRIENDS")
)
class Post(models.Model):
    post_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=True)
    title = models.CharField(max_length=200, blank=True, null=True, default='Title not specified')#
    source = models.URLField(null=True, blank=True, default=HOSTNAME)#
    origin = models.URLField(default=HOSTNAME)#
    content = models.CharField(max_length=200,choices=CONTENT,blank=True )#
    visibility = models.CharField(max_length=20, choices=VISIBILITY,blank=True)#
    creater = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    date_created = models.DateTimeField(default=timezone.now)
    content_text = models.TextField(max_length=140, blank=True)
    content_image = models.ImageField(upload_to='posts/', blank=True)
    categories = models.TextField(default='[]', null=True)
    image_url = models.URLField(null=True, blank=True)#
    likers = models.ManyToManyField(Author,blank=True , related_name='likes')
    comment_count = models.IntegerField(default=0)
    unlisted = models.BooleanField(default=False)

    def __str__(self):
        return f"Post user: {self.postid} (creater: {self.creater})"

    def img_url(self):
        return self.content_image.url

    def append(self, name, value):
        self.name = value

    def get_id(self):
        return self.origin + "authors/" + str(self.author.id) + "/posts/" + str(self.id)

    def get_source(self):
        source = str(self.source) if self.source is not None else HOSTNAME
        return source + "posts/" + str(self.id)

    def get_origin(self):
        return str(self.origin) + "posts/" + str(self.id)



    def __str__(self):
        return self.title

    @property
    def type(self):
        return 'post'
    

TYPE_CHOICES = (
    ('post','post'),
    ("comment","comment"),
    ('like','like'),
    ("follow","follow")
)
class Like(models.Model):


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

class Inbox(models.Model):


    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    object_type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True )
    object_id = models.UUIDField(null=True)
    published = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=500, default="No message")

    class Meta:
        ordering = ['-published']


