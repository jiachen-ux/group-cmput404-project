from django.conf import settings
from rest_framework import serializers
from .models import Post

MAX_POST_LENGTH = settings.MAX_POST_LENGTH
POST_ACTION_OPTIONS = settings.POST_ACTION_OPTIONS
class PostActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action= serializers.CharField()
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','content']

    def validate_content(self, value):
        if len(value) > MAX_POST_LENGTH :
            raise serializers.ValidationError("This Post is too long")
        return value


##############