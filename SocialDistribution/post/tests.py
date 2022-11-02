from django.test import TestCase
from author.models import Author
from post.models import Post
from django.utils import timezone

class TestPost(TestCase):

    def test_create_post(self):
        Post.objects.all().delete()
        Author.objects.all().delete()
        author = Author.objects.create_user(username="Test Author", password="testpassword")
        postid = author.userid

        post = Post.objects.create(creater=author,content_image="no source", content_text="still idk", comment_count= 123)
        self.assertTrue(Post.objects.filter(id=post.id)) 
