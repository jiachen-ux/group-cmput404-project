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


class AuthorCreate(
    generics.CreateAPIView
):

    # queryset = Author.objects.all()
    serializer_class = AuthorRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAuthorData(generics.ListAPIView):

    queryset = Author.objects.all()
    # serializer_class = GetAuthorSerializer
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = GetAuthorSerializer(queryset, many=True)

        return response.Response(serializer.data)


@api_view(["GET"])
def getAllAuthors(request):
    allAuthors = Author.objects.all()
    serializer = GetAuthorSerializer(allAuthors, many=True)
    resp = {
        "type": "authors",
        "items": serializer.data
    }
    return response.Response(resp)


@api_view(["GET", "POST"])
def getSingleAuthor(request, uuidOfAuthor):
    # Get single author
    singleAuthor = Author.objects.get(id=uuidOfAuthor)
    if request.method == "GET":
        serializer = GetAuthorSerializer(singleAuthor)
        return response.Response(serializer.data)
    # Update single author
    elif request.method == "POST":
        serializer = GetAuthorSerializer(
            instance=singleAuthor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return response.Response(serializer.data)

@api_view(["GET", "PUT", "POST", "DELETE"])
@permission_classes([AllowAny])
def testAuth(request):
    resp = {
        "method": request.method,
        "user": str(request.user),
        "isAuthenticated": request.user.is_authenticated,
    }
class AuthorSearchView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = GetAuthorSerializer

    def list(self, request, *args, **kwargs):
        queryset = Author.objects.filter(
            username__icontains=request.GET.get('username'))
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)