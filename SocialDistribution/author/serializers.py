from ast import mod
from pyexpat import model
from re import A
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate



class AuthorRegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = Author
        fields = ('username', 'password', 'displayName', 'github')
         
    def create(self, validated_data):
        return Author.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):

    username =  serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = Author
        fields = ('username', 'password', 'token')
        read_only_field = ['token']
        
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        author = authenticate(
            request=self.context.get('request'),
            username = username,
            password = password,
        )
        if not author:
            raise serializers.ValidationError({"Error": "Incorrect credentials provided."})
        
        attrs['user'] = author
        
        return attrs



class GetAuthorSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="url", read_only=True)
    type = serializers.CharField(read_only=True)
    url = serializers.CharField(read_only=True)
    displayName = serializers.CharField(allow_null=True)
    github = serializers.URLField(allow_blank=True, allow_null=True)
    class Meta:
        model = Author
        fields = ["type","id","host","displayName","url","github","profileImage", "username"]