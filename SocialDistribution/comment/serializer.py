from ast import mod
from pyexpat import model
from re import A
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from author.serializers import GetAuthorSerializer
from post.serializers import PostSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = GetAuthorSerializer("author", read_only=True)
    # this post is needed becoz i want to get the details about the post for sending a request in the inbox
    post = PostSerializer("post", read_only=True)
    id = serializers.CharField(source="get_id", read_only=True)
    class Meta:
        model = Comment
        fields = ["type", "author", "post", "comment", "contentType", "published", "id"]
    
    def create(self, validated_data):
        validated_data['author'] = self.context.get('author')
        validated_data['post'] = self.context.get('post') 
        return super().create(validated_data)