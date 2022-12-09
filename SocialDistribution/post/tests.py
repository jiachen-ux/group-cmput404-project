from django.test import TestCase, Client
from post.models import Post
from author.models import Author
from django.utils import timezone
from django.core import serializers
import json
import uuid
import re
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import LiveServerTestCase


from rest_framework import status 
from rest_framework.test import APIClient
from django.db import IntegrityError
from comment.models import Comment
# Create your tests here.

""" Command line examples for executing tests
Run specified module: python3 manage.py test posts.tests
"""


class PostTest(TestCase):

    def setUp(self):
        self.c = Client()

        self.url_allposts = reverse('post:index')
        self.url_createPosts = reverse('post:createpost')


    ## include the right author auth
    def test_create_post(self):
        Post.objects.all().delete()
        Author.objects.all().delete()
        author = Author.objects.create_user(username="testAuthor", password="testpassword")
        published = timezone.now()
        authorJson = json.loads(serializers.serialize('json', Author.objects.filter(id=author.id), fields=('username', 'password', 'displayName', 'github',)))[0]['fields']

        uid = uuid.uuid4()
        #postid = authorJson.get("id") + '/posts/' + uid

        post = Post.objects.create(id=uid, author=author, title="post with auth", source="no source", origin="still idk", description="not available", contentType="plain", count=0, visibility="Public", unlisted="False", published=published, content="this should be valid content")
        poststuff = json.loads(serializers.serialize('json', Post.objects.filter(id=post.id), fields=( 'type','title','id','source','origin','description','contentType','content','author','categories','count','size','comments','published','visibility', 'unlisted',)))[0]['fields']
        self.assertTrue(Post.objects.filter(id=post.id)) 


    def test_markdown(self):

        Post.objects.all().delete()
        Author.objects.all().delete()
        author = Author.objects.create_user(username="testAuthor", password="testpassword")
        published = timezone.now()
        authorJson = json.loads(serializers.serialize('json', Author.objects.filter(id=author.id), fields=('username', 'password', 'displayName', 'github',)))[0]['fields']

        uid = uuid.uuid4()
        #postid = authorJson.get("id") + '/posts/' + uid

        post = Post.objects.create(id=uid, author=author, title="post with auth", source="no source", origin="still idk", description="not available", contentType="markdown", count=0, visibility="Public", unlisted="False", published=published, content="this should be valid content")
        poststuff = json.loads(serializers.serialize('json', Post.objects.filter(id=post.id), fields=( 'type','title','id','source','origin','description','contentType','content','author','categories','count','size','comments','published','visibility', 'unlisted',)))[0]['fields']
        self.assertTrue(Post.objects.filter(id=post.id)) 

    def test_post_detail_GET(self):
        author = Author.objects.create_user(username="testAuthor", password="testpassword")
        newPost = Post(title='testpost', description="This is a new post", content="testpost", contentType="text/plain", author=author)
        newPost.save()
        response = self.c.get(reverse('post:postdetail', kwargs={'post_id':newPost.id}))

        self.assertEquals(response.status_code, 200)

        self.assertTemplateUsed(response, "index.html")


    def test_all_post_GET(self):

        response = self.c.get(self.url_allposts)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    
    def test_post_GET(self):

        response = self.c.get(self.url_createPosts)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "create.html")

    def test_post_POST(self):
        # currAuthor = Author.objects.filter(id="johnny")[0]
        # newPost = Post(title='testpost', description="This is a new post", contentType="text", author=currAuthor, categories="test")

        response = self.c.post(self.url_createPosts,{
            'title':'testpost', 
            'description':"This is a new post", 
            'contentType':"text/plain",
            'content':"testpost", 
            'unparsedCategories':"test", 
            'visibility': "PUBLIC",
            'unlisted': False,
            'postImage':'',
        })

        self.assertEquals(response.status_code, 200)
        author = Author.objects.create_user(username="testAuthor", password="testpassword")
        newPost = Post(title='testpost', description="This is a new post", content="testpost", contentType="text/plain", author=author)
        self.assertEquals(newPost.description, "This is a new post")
        self.assertEquals(newPost.title, "testpost")


    def test_post_edit(self):
        '''
        Tests for editing an post
        '''
        author = Author.objects.create_user(username="testAuthor", password="testpassword")
        newPost = Post(title='testpost', description="This is a new post", content="testpost", contentType="text/plain", author=author)
        newPost.save()
        

        editPost = Post.objects.get(author__username='testAuthor')
        self.assertNotEquals(editPost.title, "title edited")
        self.assertNotEquals(editPost.content, "content edited")


    def test_post_delete(self):
        '''
        Test deleting a post
        '''
        author = Author.objects.create_user(username="testAuthor", password="testpassword")
        newPost = Post(title='testpost', description="This is a new post", content="testpost", contentType="text/plain", author=author)
        newPost.save()
        
        
        response = self.c.post(reverse('post:deletepost', kwargs={'post_id':newPost.id}),{
        })

        deletedPost = Post.objects.get(author__username='testAuthor')
        self.assertEqual(response.status_code,200)

    def test_CommentsAPIView_GET(self):
        '''
        tsting comments on Posts
        '''
        author = Author.objects.create_user(username="testAuthor", password="testpassword")
        newPost = Post(title='testpost', description="This is a new post", content="testpost", contentType="text/plain", author=author)
        newPost.save()

        sample_comment = Comment(comment="This is a new comment", contentType="text/plain", author=author, post=newPost)
        sample_comment.id = uuid.uuid4()
        sample_comment.save()

        response = self.c.get(reverse('post:postdetail', kwargs={'post_id':newPost.id}))
        self.assertEqual(response.status_code,200)
        self.assertEqual("This is a new comment", sample_comment.comment)

    def test_CommentsAPIView_POST(self):
        author = Author.objects.create_user(username="testAuthor", password="testpassword")
        newPost = Post(title='testpost', description="This is a new post", content="testpost", contentType="text/plain", author=author)
        newPost.save()

        response = self.client.post(reverse('post:postdetail', kwargs={'post_id':newPost.id}))
        self.assertEqual(response.status_code,200)
