from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
from django.contrib.auth import authenticate,login,logout
from .models import *
from follower.models import Follower
from post.models import Post
from rest_framework.decorators import api_view
from rest_framework.generics  import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework import serializers
from .serial import  *

def index(request):
    all_posts = Post.objects.all().order_by('-date_created')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 1
    posts = paginator.get_page(page_number)
    followings = []
    suggestions = []
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = Author.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
    return render(request, "index.html", {
        "posts": posts,
        "suggestions": suggestions,
        "page": "all_posts",
        'profile': False
    })

@api_view(['POST','GET'])
def login_view(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        displayName = request.POST["displayName"]
        github= request.POST["github"]
        if password != confirmation:
            return render(request, "signup.html", {
                "message": "Passwords must match."
            })
        try:
            user = Author.objects.create_user(username,password,displayName,github)
            Follower.objects.create(user=user)
        except IntegrityError:
            return render(request, "signup.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "signup.html")


class ProfileView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = GetAuthorSerializer

class SingleProfileView(RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all() 
    serializer_class = GetAuthorSerializer
    def get_object(self):
        return Author.objects.get(userid=self.kwargs.get("uuid"))



def profile(request, userid):
    user = Author.objects.get(userid=userid)  
    all_posts = Post.objects.filter(creater=user).order_by('-date_created')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 1
    posts = paginator.get_page(page_number)
    followings = []
    suggestions = []
    follower = False
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = Author.objects.exclude(pk__in=followings).exclude(userid=request.user.userid).order_by("?")[:6]

        if request.user in Follower.objects.get(user=user).followers.all():
            follower = True
    
    follower_count = Follower.objects.get(user=user).followers.all().count()
    following_count = Follower.objects.filter(followers=user).count()
    return render(request, 'profile.html', {
        "username": user,
        "posts": posts,
        "posts_count": all_posts.count(),
        "suggestions": suggestions,
        "page": "profile",
        "is_follower": follower,
        "follower_count": follower_count,
        "following_count": following_count
    })
