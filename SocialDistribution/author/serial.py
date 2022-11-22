from ast import mod
from pyexpat import model
from re import A
from rest_framework import serializers
from .models import *

class GetAuthorSerializer(serializers.ModelSerializer):
    userid = serializers.CharField(source="url", read_only=True)
    url = serializers.CharField(read_only=True)
    displayName = serializers.CharField(allow_null=True)
    github = serializers.URLField(allow_blank=True, allow_null=True)
    class Meta:
        model = Author
        fields = ["type","userid","host","displayName","url","github","profile_pic"]

class GetSingleAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["type","userid","host","displayName","url","github","profile_pic"]


