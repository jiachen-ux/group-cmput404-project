from rest_framework import serializers
from .models import Author, POST

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('type', 'userId', 'url', 'host', 'displayName', 'github', 'profileImage')


 
 
 
 

# MAX_POST_LENGTH = settings.MAX_POST_LENGTH
# POST_ACTION_OPTIONS = settings.POST_ACTION_OPTIONS
class PostActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action= serializers.CharField()
    def validate_action(self, value):
        value = value.lower().strip()
        return value
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = POST
        fields = ['id','content']

    def validate_content(self, value):
        if len(value) > 500 :
            raise serializers.ValidationError("This Post is too long")
        return value

