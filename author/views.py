from django.shortcuts import render
from rest_framework import generics
from .serializers import AuthorSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import models
 
from rest_framework.permissions import AllowAny


class AuthorCreateView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    queryset = models.Author.objects.all()
    serializer_class = AuthorSerializer

    def post(self, request, *args, **kwargs):
        print(request.method)
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
# Create your views here.
