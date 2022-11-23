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
from post.models import Inbox


@api_view(["GET", "PUT", "DELETE"])
def handleFollowRequest(request, sender, receiver):
    # Ensure that there is a follow request from sender to reciever
    if request.method == "GET":
        try:
            followReqObj = FollowRequest.objects.get(
                sender__id=sender, receiver__id=receiver)
            returnObj = SingleFollowRequestSerializer(followReqObj).data
            return response.Response(returnObj, 200)

        except:
            return response.Response({"message": "Following relationship does not exists!"}, 404)

    # Add follow request from sender to reciever
    if request.method == "PUT":
        try:
            newFollowReqObj = FollowRequest.objects.get_or_create(
                sender_id=sender, receiver_id=receiver)
            returnObj = SingleFollowRequestSerializer(newFollowReqObj[0])
            return response.Response(returnObj.data, status=status.HTTP_201_CREATED)
        except:
            return response.Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Delete follow request from sender to reciever:
    if request.method == "DELETE":
        try:
            FollowRequest.objects.filter(
                sender__id=sender, receiver__id=receiver).delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return response.Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(["GET", "PUT", "DELETE"])
def handleSingleFollow(request, authorID, foreignAuthor):

    if request.method == "GET":
        try:
            followObject = Follower.objects.get(
                follower__id=foreignAuthor, following__id=authorID)
            s = SingleFollowerSerializer(followObject)
            return response.Response(s.data, 200)
        except:
            return response.Response({"message": "Following relationship does not exists!"}, 404)

    if request.method == "PUT":
        try:
            if not request.user.is_authenticated:
                return response.Response({"message": "Unauthorized"}, status.HTTP_401_UNAUTHORIZED)

            newFollowObj = Follower.objects.get_or_create(
                follower_id=foreignAuthor, following_id=authorID)
            serializer = SingleFollowerSerializer(newFollowObj[0])
            Inbox.objects.create(author_id=foreignAuthor,
                                 object_type="following", object_id=authorID, message=f"{request.user.username} accepted your follow request.")
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return response.Response({"message": "Following relationship does not exists!"}, 404)

    if request.method == "DELETE":
        try:
            followObj = Follower.objects.filter(
                follower__id=foreignAuthor, following__id=authorID).delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return response.Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)