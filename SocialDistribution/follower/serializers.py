
from functools import partial
import json
from re import A
import re
from . import utils
from django.shortcuts import render
from rest_framework import generics, mixins, response, status
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from base64 import b64encode

from ast import mod
from pyexpat import model
from re import A
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from author.serializers import GetAuthorSerializer

class FollowerSerializer(serializers.ModelSerializer):
    follower = GetAuthorSerializer(read_only=True)
    class Meta:
        model = Follower
        fields = ["follower"]


class SingleFollowerSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    follower = GetAuthorSerializer(read_only=True)
    following = GetAuthorSerializer(read_only=True)
    class Meta:
        model = Follower
        fields = ["id","follower","following","timestamp"]

class SingleFollowRequestSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField()
    sender = GetAuthorSerializer()
    receiver = GetAuthorSerializer()
    class Meta:
        model = FollowRequest
        fields = ["id","sender","receiver","timestamp"]

@api_view(["GET"])
def getAllFollowers(request, uuidOfAuthor):
    # Get multiple follower objects
    allFollowers = Follower.objects.filter(following__id=uuidOfAuthor)
    serializer = FollowerSerializer(allFollowers, many=True)
    resp = {
        "type": "followers",
        "items": [obj["follower"] for obj in serializer.data]
    }
    return response.Response(resp)