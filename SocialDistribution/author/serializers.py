from ast import mod
from pyexpat import model
from re import A
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class AuthorRegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = Author
        fields = ('username', 'password', 'displayName', 'github')
         
    def create(self, validated_data):
        return Author.objects.create_user(**validated_data)


class LoginSerializer(TokenObtainPairSerializer):
 
    def validate(self, attrs):
        data =  super().validate(attrs)

        data['username'] = self.user.username
        data['id'] = self.user.id
        data['github'] = self.user.github
        data['displayName'] = self.user.displayName
 
        return data

class GetAuthorSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="url", read_only=True)
    type = serializers.CharField(read_only=True)
    url = serializers.CharField(read_only=True)
    displayName = serializers.CharField(allow_null=True)
    github = serializers.URLField(allow_blank=True, allow_null=True)
    class Meta:
        model = Author
        fields = ["type","id","host","displayName","url","github","profileImage", "username"]