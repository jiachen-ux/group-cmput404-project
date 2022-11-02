from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from uuid import uuid4
from .models import Post
from .serializers import PostSerializer
from authors.models import Author

# Create your views here.
class PostApiView(APIView):
    def get(self, request: Request, author_id: str = None, post_id: str = None):
        if author_id == None:
            posts = list(Post.objects.filter(visibility='PUBLIC', unlisted=False).order_by('-published'))
            serializer =  PostSerializer(posts, many=True)
            res = {"items": serializer.data}
            return Response(res)
        try:
            author = Author.objects.get(userId = author_id)
        except Exception as e:
            return Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
        if author == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if post_id == None:
            posts = list(Post.objects.filter(author = author).order_by("-published"))
            serializer = PostSerializer(posts, many=True)
            result = {"items": serializer.data}
            return Response(result, status=status.HTTP_200_OK)
        else:
            try:
                postObj = Post.objects.get(id = post_id, author = author, visibility='PUBLIC')
                serializer = PostSerializer(postObj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request: Request, author_id: str, post_id: str = None):
        try:
            author = Author.objects.get(userId = author_id)
        except Exception as e:
            return Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
        if author == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # Update a post
        if post_id is not None:
            try: 
                author = Author.objects.get(userId=author_id)
                post = Post.objects.get(id = post_id, author=author)
                serializer = PostSerializer(post, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.validated_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
        else:
            serialize = PostSerializer(data=request.data)
            if serialize.is_valid(raise_exception=True):
                try:
                    author = Author.objects.get(userId=author_id)
                    ID = str(uuid4())
                    
                    serialize.save(
                        id=ID,
                        author=author,
                        )
                    return Response(serialize.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request: Request, author_id: str, post_id: str):
        try:
            author = Author.objects.get(userId = author_id)
        except Exception as e:
            return Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
        if author == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            post = Post.objects.get(id=post_id, author=author)
            post.delete()
            return Response("Post was deleted Successfully", status.HTTP_200_OK)
        except Exception as e:
                return Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)


        

