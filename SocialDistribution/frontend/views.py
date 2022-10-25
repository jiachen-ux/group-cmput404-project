from turtle import pos
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from .models import Post
import random

from .forms import PostForm
from .serializers import PostSerializer

ALLOWED_HOSTS =settings.ALLOWED_HOSTS

def index(request, *args, **kwargs):
   #return render(request, 'frontend/index.html')
    return render(request, "pages/home.html", context={},status=200)

@api_view(['POST'])
@authentication_classes([IsAuthenticated])
#@permission_classes([IsAuthenticated])
def post_create_view(request, *args, **kwargs):
    serializer = PostSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return JsonResponse(serializer.data, status=201)
    return Response({}, status=400)

@api_view(["GET"])
def post_detail_view(request, *args, **kwargs):
    qs = Post.objects.all() #list
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = PostSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(["GET"])
def post_list_view(request, *args, **kwargs):
    qs = Post.objects.all() #list
    serializer = PostSerializer(qs, many=True)
    return Response(serializer.data, status=200)

@api_view(["DELETE", "POST"])
def post_delete_view(request, *args, **kwargs):
    qs = Post.objects.filter(id=post_id) #list
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"messages": "You cannot delere this post"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Post removed"}, status=200)
