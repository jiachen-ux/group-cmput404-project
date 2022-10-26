# Create your views here.
from django.shortcuts import  render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import generics
from .models import Author 
from .serializers import AuthorSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from uuid import uuid4
from .models import POST
from .serializers import PostSerializer
 

def login_page(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                # return redirect("authors:homepage") <- this should redirect to a page that show's user's main page
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    context = {"login_form":form}
    return render(request, "authors/login.html", context)


def register_page(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful." )
            return redirect('/login')
        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = UserRegisterForm()
    context = {'register_form': form}

    return render(request, 'authors/register.html', context)


class AuthorView (generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    

from turtle import pos
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from .models import POST
import random

from .forms import PostForm
from .serializers import PostSerializer

ALLOWED_HOSTS =settings.ALLOWED_HOSTS

def index(request, *args, **kwargs):
   #return render(request, 'frontend/index.html')
    return render(request, "pages/home.html", context={},status=200)

@api_view(['POST'])
# @authentication_classes([IsAuthenticated])
#@permission_classes([IsAuthenticated])
def post_create_view(request, *args, **kwargs):
    serializer = PostSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return JsonResponse(serializer.data, status=201)
    return Response({}, status=400)

@api_view(["GET"])
def post_detail_view(request, *args, **kwargs):
    qs = POST.objects.all() #list
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = PostSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(["GET"])
def post_list_view(request, *args, **kwargs):
    qs = POST.objects.all() #list
    serializer = PostSerializer(qs, many=True)
    return Response(serializer.data, status=200)

@api_view(["DELETE", "POST"])
def post_delete_view(request, *args, **kwargs):
    qs = POST.objects.filter(id=post_id) #list
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"messages": "You cannot delere this post"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Post removed"}, status=200)
