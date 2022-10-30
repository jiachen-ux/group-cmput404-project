from rest_framework import serializers
from . import models

class AuthorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255)
    class Meta:
        model = models.Author
        fields = ['username', 'password']


