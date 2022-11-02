from django.test import TestCase
from author.models import Author
from post.models import Post
from django.utils import timezone

import json
import uuid
import re


from rest_framework import status 
from rest_framework.test import APIClient
from django.db import IntegrityError
from django.core import serializers

# # Create your tests here.
# class PostViewTestCases(TestCase):
#      @classmethod
#      def setUpData(cls):
#         uuids = [
#             "e84c8098-c240-48c2-91d9-1d266a0cd371",
#             "e84c8098-c240-48c2-91d9-1d266a0cd372",
#         ]
#         authors = []
#         for index in range(len(uuids)):
#             authors.append(Author.objects.create(
#                 userId=uuids[index],
#                 username = "PostTestCase{}".format(index),
#                 display_name="Test object{}".format(index),
#                 url="https://cmput-404-social-distribution.herokuapp.com/author/{}".format(uuids[index]),
#                 host="https://cmput-404-social-distribution.herokuapp.com/",
#             ))

class TestPost(TestCase):

    def test_create_post(self):
        Post.objects.all().delete()
        Author.objects.all().delete()
        author = Author.objects.create_user(username="Test Author", password="testpassword")
        postid = author.userid

        post = Post.objects.create(id=postid, author=author, title="post with auth", source="no source", origin="still idk", description="not available", contentType="plain", count=0, visibility="Public", unlisted="False", content="this should be valid content")
        self.assertTrue(Post.objects.filter(id=post.id)) 

