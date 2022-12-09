from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *
from comment.models import *
from post.models import *
from like.models import *
from follower.models import *
from datetime import date
import json


class AuthorRoutesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        uuid_tests = [
            "631f3ebe-d976-4248-a808-db2442a22168",
            "ca14e1e3-77ce-44e3-8529-85172744c45b",
        ]
        for i in range(len(uuid_tests)):
            Author.objects.create(
                username="Author User Name" + str(i),
                displayName="Author Display Name " + str(i),
                id=uuid_tests[i],
            )
    
    def testNotRealAuthor(self):
        res = self.client.get("/author/282848/")
        self.assertEqual(res.status_code, 404)
    

 
class FollowersRoutesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        uuid_tests = [
            "631f3ebe-d976-4248-a808-db2442a22168",
            "ca14e1e3-77ce-44e3-8529-85172744c45b",
        ]
        
        authors = []
        
        for i in range(len(uuid_tests)):
            authors.append(Author.objects.create(
                username="Author User Name" + str(i),
                displayName="Author Display Name " + str(i),
                id=uuid_tests[i],
            ))
            
        Follower.objects.create(
        id = "5cdfd032-7d84-446f-9a60-c451212ad0a6",
        follower = authors[0],
        following = authors[1],
        )



class PostRoutesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        uuid_tests = [
            "631f3ebe-d976-4248-a808-db2442a22168",
            "ca14e1e3-77ce-44e3-8529-85172744c45b",
        ]
        authors = []

        for i in range(len(uuid_tests)):
            authors.append(Author.objects.create(
                username="Author User Name" + str(i),
                displayName="Author Display Name " + str(i),
                id=uuid_tests[i],
            ))
        Post.objects.create(
            id="631f3ebe-d976-4248-a808-db2442a22169",
            image_url="http://127.0.0.1:8000/author/631f3ebe-d976-4248-a808-db2442a22168/post/631f3ebe-d976-4248-a808-db2442a22169",
            title="Post Title 1",
            source="https://github.com/CMPUT404F22T01/",
            origin="https://github.com/CMPUT404F22T01/",
            description="Post description 1",
            contentType="text/plain",
            content="Post content 1",
            author=authors[0],
        )
        
        Post.objects.create(
            id="631f3ebe-d976-4248-a808-db2442a22167",
            image_url="http://127.0.0.1:8000/author/ca14e1e3-77ce-44e3-8529-85172744c45b/post/631f3ebe-d976-4248-a808-db2442a22167",
            title="Post Title 2",
            source="https://github.com/CMPUT404F22T01/",
            origin="https://github.com/CMPUT404F22T01/",
            description="Post description 2",
            contentType="text/plain",
            content="Post content 2",
            author=authors[1],
        )

  

class CommentRoutesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        uuid_tests = [
            "631f3ebe-d976-4248-a808-db2442a22168",
            "ca14e1e3-77ce-44e3-8529-85172744c45b",
        ]
        authors = []

        for i in range(len(uuid_tests)):
            authors.append(Author.objects.create(
                username="Author User Name" + str(i),
                displayName="Author Display Name " + str(i),
                id=uuid_tests[i],
            ))
            
        aPost = Post.objects.create(
            id="631f3ebe-d976-4248-a808-db2442a22169",
            image_url="http://127.0.0.1:8000/author/631f3ebe-d976-4248-a808-db2442a22168/post/631f3ebe-d976-4248-a808-db2442a22169",
            title="Post Title 1",
            source="https://github.com/CMPUT404F22T01/",
            origin="https://github.com/CMPUT404F22T01/",
            description="Post description 1",
            contentType="text/plain",
            content="Post content 1",
            author=authors[0],
        )
        
        Comment.objects.create(
        id="77fce8fb-3439-4010-b854-0f6fd44c9c3f",
        author = authors[1],
        post = aPost,
        comment = "Comment 1",
        )
    
        
class LikesAndLikedTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        uuid_tests = [
            "631f3ebe-d976-4248-a808-db2442a22168",
            "ca14e1e3-77ce-44e3-8529-85172744c45b",
        ]
        authors = []

        for i in range(len(uuid_tests)):
            authors.append(Author.objects.create(
                username="Author User Name" + str(i),
                displayName="Author Display Name " + str(i),
                id=uuid_tests[i],
            ))
        aPost = Post.objects.create(
            id="631f3ebe-d976-4248-a808-db2442a22169",
            image_url="http://127.0.0.1:8000/author/631f3ebe-d976-4248-a808-db2442a22168/post/631f3ebe-d976-4248-a808-db2442a22169",
            title="Post Title 1",
            source="https://github.com/CMPUT404F22T01/",
            origin="https://github.com/CMPUT404F22T01/",
            description="Post description 1",
            contentType="text/plain",
            content="Post content 1",
            author=authors[0],
        )
        postLike = Like.objects.create(
            id = "3a49d082-9b61-4972-8d22-0066e4aea309",
            object_id = "631f3ebe-d976-4248-a808-db2442a22169",
            author = authors[1],
            object_type = "post",
        )
        
        aComment = Comment.objects.create(
        id="77fce8fb-3439-4010-b854-0f6fd44c9c3f",
        author = authors[1],
        post = aPost,
        comment = "Comment 1",
        )
        
        commentLike = Like.objects.create(
            id = "4695f35e-9e01-4cc1-ba66-450c378b2b64",
            object_id = aComment.id,
            author = authors[1],
            object_type = "comment",
        )
        


    

    
###### MODEL TESTS ######
class AuthorTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        uuid_tests = [
            "631f3ebe-d976-4248-a808-db2442a22168",
            "ca14e1e3-77ce-44e3-8529-85172744c45b",
        ]
        for i in range(len(uuid_tests)):
            Author.objects.create(
                username="Author User Name" + str(i),
                displayName="Author Display Name " + str(i),
                id=uuid_tests[i],
            )

    def testDisplayName(self):
        author = Author.objects.get(id="631f3ebe-d976-4248-a808-db2442a22168")
        self.assertEqual(author.displayName, 'Author Display Name 0')
        author = Author.objects.get(id="ca14e1e3-77ce-44e3-8529-85172744c45b")
        self.assertEqual(author.displayName, 'Author Display Name 1')

    def testHost(self):
        author = Author.objects.get(id="631f3ebe-d976-4248-a808-db2442a22168")
        self.assertEqual(author.host, HOSTNAME)
        author = Author.objects.get(id="ca14e1e3-77ce-44e3-8529-85172744c45b")
        self.assertEqual(author.host, HOSTNAME)


class PostsTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        uuid_tests = [
            "631f3ebe-d976-4248-a808-db2442a22168",
            "ca14e1e3-77ce-44e3-8529-85172744c45b",
        ]
        authors = []

        for i in range(len(uuid_tests)):
            authors.append(Author.objects.create(
                username="Author User Name" + str(i),
                displayName="Author Display Name " + str(i),
                id=uuid_tests[i],
            ))
        Post.objects.create(
            id="631f3ebe-d976-4248-a808-db2442a22169",
            image_url="http://127.0.0.1:8000/author/631f3ebe-d976-4248-a808-db2442a22168/post/631f3ebe-d976-4248-a808-db2442a22169",
            title="Post Title 1",
            source="https://github.com/CMPUT404F22T01/",
            origin="https://github.com/CMPUT404F22T01/",
            description="Post description 1",
            contentType="text/plain",
            content="Post content 1",
            author=authors[0],
        )
        
        Post.objects.create(
            id="631f3ebe-d976-4248-a808-db2442a22167",
            image_url="http://127.0.0.1:8000/author/ca14e1e3-77ce-44e3-8529-85172744c45b/post/631f3ebe-d976-4248-a808-db2442a22167",
            title="Post Title 2",
            source="https://github.com/CMPUT404F22T01/",
            origin="https://github.com/CMPUT404F22T01/",
            description="Post description 2",
            contentType="text/plain",
            content="Post content 2",
            author=authors[1],
        )

    def testTitle(self):
        post = Post.objects.get(id="631f3ebe-d976-4248-a808-db2442a22169")
        self.assertEqual(post.title, 'Post Title 1')
        post = Post.objects.get(id="631f3ebe-d976-4248-a808-db2442a22167")
        self.assertEqual(post.title, 'Post Title 2')

    def testImageUrl(self):
        post = Post.objects.get(id="631f3ebe-d976-4248-a808-db2442a22169")
        self.assertEqual(post.image_url, "http://127.0.0.1:8000/" + "author/631f3ebe-d976-4248-a808-db2442a22168/post/631f3ebe-d976-4248-a808-db2442a22169")
        post = Post.objects.get(id="631f3ebe-d976-4248-a808-db2442a22167")
        self.assertEqual(post.image_url, "http://127.0.0.1:8000/" + "author/ca14e1e3-77ce-44e3-8529-85172744c45b/post/631f3ebe-d976-4248-a808-db2442a22167")

    def testSource(self):
        post = Post.objects.get(id="631f3ebe-d976-4248-a808-db2442a22169")
        self.assertEqual(post.source, 'https://github.com/CMPUT404F22T01/')
        post = Post.objects.get(id="631f3ebe-d976-4248-a808-db2442a22167")
        self.assertEqual(post.source, 'https://github.com/CMPUT404F22T01/')
        
    def testOrigin(self):
        post = Post.objects.get(id="631f3ebe-d976-4248-a808-db2442a22169")
        self.assertEqual(post.origin, 'https://github.com/CMPUT404F22T01/')
        post = Post.objects.get(id="631f3ebe-d976-4248-a808-db2442a22167")
        self.assertEqual(post.source, 'https://github.com/CMPUT404F22T01/')
        
    def testDescription(self):
        post = Post.objects.get(id="631f3ebe-d976-4248-a808-db2442a22169")
        self.assertEqual(post.description, 'Post description 1')
        post = Post.objects.get(id="631f3ebe-d976-4248-a808-db2442a22167")
        self.assertEqual(post.description, 'Post description 2')
        
    def testContent(self):
        post = Post.objects.get(id="631f3ebe-d976-4248-a808-db2442a22169")
        self.assertEqual(post.content, 'Post content 1')
        post = Post.objects.get(id="631f3ebe-d976-4248-a808-db2442a22167")
        self.assertEqual(post.content, 'Post content 2')
        
    def testAuthor(self):
        post = Post.objects.get(id="631f3ebe-d976-4248-a808-db2442a22169")
        self.assertEqual(str(post.author.id), '631f3ebe-d976-4248-a808-db2442a22168')
        post = Post.objects.get(id="631f3ebe-d976-4248-a808-db2442a22167")
        self.assertEqual(str(post.author.id), 'ca14e1e3-77ce-44e3-8529-85172744c45b')
  
class CommentsTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        uuid_tests = [
            "631f3ebe-d976-4248-a808-db2442a22168",
            "ca14e1e3-77ce-44e3-8529-85172744c45b",
        ]
        authors = []

        for i in range(len(uuid_tests)):
            authors.append(Author.objects.create(
                username="Author User Name" + str(i),
                displayName="Author Display Name " + str(i),
                id=uuid_tests[i],
            ))
            
        aPost = Post.objects.create(
            id="631f3ebe-d976-4248-a808-db2442a22169",
            image_url="http://127.0.0.1:8000/author/631f3ebe-d976-4248-a808-db2442a22168/post/631f3ebe-d976-4248-a808-db2442a22169",
            title="Post Title 1",
            source="https://github.com/CMPUT404F22T01/",
            origin="https://github.com/CMPUT404F22T01/",
            description="Post description 1",
            contentType="text/plain",
            content="Post content 1",
            author=authors[0],
        )
        
        Comment.objects.create(
        id="77fce8fb-3439-4010-b854-0f6fd44c9c3f",
        author = authors[1],
        post = aPost,
        comment = "Comment 1",
        )
        
    def testComment(self):
        aComment = Comment.objects.get(id="77fce8fb-3439-4010-b854-0f6fd44c9c3f")
        self.assertEqual(aComment.comment, "Comment 1")   
        
    def testUrl(self):
        aComment = Comment.objects.get(id="77fce8fb-3439-4010-b854-0f6fd44c9c3f")
        self.assertEqual(aComment.get_id(), "https://github.com/CMPUT404F22T01/authors/ca14e1e3-77ce-44e3-8529-85172744c45b/posts/631f3ebe-d976-4248-a808-db2442a22169/comments/77fce8fb-3439-4010-b854-0f6fd44c9c3f")
    
    def testCommentAuthor(self):
        aComment = Comment.objects.get(id="77fce8fb-3439-4010-b854-0f6fd44c9c3f")
        self.assertEqual(str(aComment.author.id), "ca14e1e3-77ce-44e3-8529-85172744c45b")
    
    def testCommentPostAuthor(self):
        aComment = Comment.objects.get(id="77fce8fb-3439-4010-b854-0f6fd44c9c3f")
        self.assertEqual(str(aComment.post.author.id), "631f3ebe-d976-4248-a808-db2442a22168")
    
class LikeTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        uuid_tests = [
            "631f3ebe-d976-4248-a808-db2442a22168",
            "ca14e1e3-77ce-44e3-8529-85172744c45b",
        ]
        authors = []

        for i in range(len(uuid_tests)):
            authors.append(Author.objects.create(
                username="Author User Name" + str(i),
                displayName="Author Display Name " + str(i),
                id=uuid_tests[i],
            ))
        aPost = Post.objects.create(
            id="631f3ebe-d976-4248-a808-db2442a22169",
            image_url="http://127.0.0.1:8000/author/631f3ebe-d976-4248-a808-db2442a22168/post/631f3ebe-d976-4248-a808-db2442a22169",
            title="Post Title 1",
            source="https://github.com/CMPUT404F22T01/",
            origin="https://github.com/CMPUT404F22T01/",
            description="Post description 1",
            contentType="text/plain",
            content="Post content 1",
            author=authors[0],
        )
        postLike = Like.objects.create(
            id = "3a49d082-9b61-4972-8d22-0066e4aea309",
            object_id = "631f3ebe-d976-4248-a808-db2442a22169",
            author = authors[1],
            object_type = "post",
        )
        
        aComment = Comment.objects.create(
        id="77fce8fb-3439-4010-b854-0f6fd44c9c3f",
        author = authors[1],
        post = aPost,
        comment = "Comment 1",
        )
        
        commentLike = Like.objects.create(
            id = "4695f35e-9e01-4cc1-ba66-450c378b2b64",
            object_id = aComment.id,
            author = authors[1],
            object_type = "comment",
        )
        
    def testLikeAuthor(self):
        aLike = Like.objects.get(id="3a49d082-9b61-4972-8d22-0066e4aea309")
        self.assertEqual(str(aLike.author.id), "ca14e1e3-77ce-44e3-8529-85172744c45b")
    
    def testPostIsLiked(self):
        aLike = Like.objects.get(id="3a49d082-9b61-4972-8d22-0066e4aea309")
        self.assertEqual(str(aLike.object_id), "631f3ebe-d976-4248-a808-db2442a22169")
      
    def testCommentIsLiked(self):
        aLike = Like.objects.get(id="4695f35e-9e01-4cc1-ba66-450c378b2b64")
        self.assertEqual(str(aLike.object_id), "77fce8fb-3439-4010-b854-0f6fd44c9c3f")
        
    def testObjectUrl(self):
        aLike = Like.objects.get(id="3a49d082-9b61-4972-8d22-0066e4aea309")
        self.assertEqual(aLike.object_url(), "https://github.com/CMPUT404F22T01/authors/631f3ebe-d976-4248-a808-db2442a22168/posts/631f3ebe-d976-4248-a808-db2442a22169")
        aLike = Like.objects.get(id="4695f35e-9e01-4cc1-ba66-450c378b2b64")
        self.assertEqual(aLike.object_url(), "https://github.com/CMPUT404F22T01/authors/ca14e1e3-77ce-44e3-8529-85172744c45b/posts/631f3ebe-d976-4248-a808-db2442a22169/comments/77fce8fb-3439-4010-b854-0f6fd44c9c3f")
        
    def testSummary(self):
        aLike = Like.objects.get(id="3a49d082-9b61-4972-8d22-0066e4aea309")
        self.assertEqual(aLike.summary(), 'Author Display Name 1 Likes your post')
        aLike = Like.objects.get(id="4695f35e-9e01-4cc1-ba66-450c378b2b64")
        self.assertEqual(aLike.summary(), 'Author Display Name 1 Likes your comment')
        
    def testTypeOfWhatIsLiked(self):
        aLike = Like.objects.get(id="3a49d082-9b61-4972-8d22-0066e4aea309")
        self.assertEqual(aLike.object_type, 'post')
        aLike = Like.objects.get(id="4695f35e-9e01-4cc1-ba66-450c378b2b64")
        self.assertEqual(aLike.object_type, 'comment')
        
class FollowerTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        uuid_tests = [
            "631f3ebe-d976-4248-a808-db2442a22168",
            "ca14e1e3-77ce-44e3-8529-85172744c45b",
        ]
        authors = []

        for i in range(len(uuid_tests)):
            authors.append(Author.objects.create(
                username="Author User Name" + str(i),
                displayName="Author Display Name " + str(i),
                id=uuid_tests[i],
            ))
            
        Follower.objects.create(
            id = "5cdfd032-7d84-446f-9a60-c451212ad0a6",
            follower = authors[0],
            following = authors[1],
        )
        
    def testFollwerFollowwing(self):
        aFollower = Follower.objects.get(id="5cdfd032-7d84-446f-9a60-c451212ad0a6")
        self.assertEquals(str(aFollower.follower.id), "631f3ebe-d976-4248-a808-db2442a22168")
        self.assertEquals(str(aFollower.following.id), "ca14e1e3-77ce-44e3-8529-85172744c45b")        
        
class FollowRequestTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        uuid_tests = [
            "631f3ebe-d976-4248-a808-db2442a22168",
            "ca14e1e3-77ce-44e3-8529-85172744c45b",
        ]
        authors = []

        for i in range(len(uuid_tests)):
            authors.append(Author.objects.create(
                username="Author User Name" + str(i),
                displayName="Author Display Name " + str(i),
                id=uuid_tests[i],
            ))
            
        FollowRequest.objects.create(
            id = "5cdfd032-7d84-446f-9a60-c451212ad0a6",
            sender = authors[0],
            receiver = authors[1],
        )
        
    def testFollwerFollowwing(self):
        aFollowRequest = FollowRequest.objects.get(id="5cdfd032-7d84-446f-9a60-c451212ad0a6")
        self.assertEquals(str(aFollowRequest.sender.id), "631f3ebe-d976-4248-a808-db2442a22168")
        self.assertEquals(str(aFollowRequest.receiver.id), "ca14e1e3-77ce-44e3-8529-85172744c45b")        


    
    
