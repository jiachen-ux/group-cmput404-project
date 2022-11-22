
from ast import mod
from pyexpat import model
from re import A
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from author.serializers import GetAuthorSerializer
from like.models import Like

class LikeSerializer(serializers.ModelSerializer): 
    type = serializers.CharField(read_only=True)
    author = GetAuthorSerializer("author", read_only=True)
    # object = serializers.CharField(source="object_url") 
    class Meta:
        model = Like
        fields = ["type", "author", "object_id"] 
 
        
class PostSerializer(serializers.ModelSerializer):
    # type = serializers.CharField(default="post", read_only=True)
    # source = serializers.CharField(source="get_source", read_only=True)
    # origin = serializers.CharField(source="get_origin", read_only=True)
    # contentType = serializers.ChoiceField(choices=Post.ContentTypeEnum.choices, default=Post.ContentTypeEnum.PLAIN)
    # visibility = serializers.ChoiceField(choices=Post.VisibilityEnum.choices, default=Post.VisibilityEnum.PUBLIC)
    

    #Method 1
    type = serializers.SerializerMethodField()
    #method 2
    # type = serializers.ReadOnlyField(default=POST.type)
    # read_only equals to true becoz we don't want users to edit the author data while changing post data
    author = GetAuthorSerializer("author", read_only=True)
    id = serializers.CharField(source="get_id", read_only=True)
    class Meta:
        model = Post
        fields = "__all__"
    
    def get_type(self, obj):
        return obj.type

    #overding the default create method in the createAPI class
    def create(self, validated_data):
       #geeting author from the context we added it and adding to validated_data 

       #check becoz for put needs it and the post method in the other post view does not need the id becoz we 
       # have default id coming from the model when we create a new post
       if self.context.get('id') is not None:
            validated_data['id'] = self.context.get('id')
       validated_data['author'] = self.context.get('author')
       return super().create(validated_data)

 