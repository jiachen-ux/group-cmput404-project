from rest_framework import serializers
<<<<<<< HEAD:author/serializers.py
from . import models

class AuthorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255)
    class Meta:
        model = models.Author
        fields = ['username', 'password']
=======
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('type', 'userId', 'url', 'host', 'displayName', 'github', 'profileImage')
>>>>>>> parent of 407ea186 (new):SocialDistribution/authors/serializers.py
