from .models import Post,Like
from rest_framework import serializers
from author.serial import GetAuthorSerializer

class LikeSerializer(serializers.ModelSerializer): 
    type = serializers.CharField(read_only=True)
    author = GetAuthorSerializer("author", read_only=True)
    # object = serializers.CharField(source="object_url") 
    class Meta:
        model = Like
        fields = ["type", "author", "object_id"] 
 
        
class PostSerializer(serializers.ModelSerializer):

    type = serializers.SerializerMethodField()
    author = GetAuthorSerializer("author", read_only=True)
    id = serializers.CharField(source="get_id", read_only=True)
    class Meta:
        model = Post
        fields = "__all__"
    
    def get_type(self, obj):
        return obj.type

    def create(self, validated_data):
       if self.context.get('id') is not None:
            validated_data['id'] = self.context.get('id')
       validated_data['author'] = self.context.get('author')
       return super().create(validated_data)
