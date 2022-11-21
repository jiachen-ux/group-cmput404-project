from functools import partial
import json
from re import A
import re
from . import utils
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from rest_framework import generics, mixins, response, status
from post.models import POST
from follower.models import Follower
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from base64 import b64encode

from author.forms import CreateAuthorForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from author.serializers import *
from django.urls import reverse


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

# def index(request):
#     all_posts = Post.objects.all().order_by('-date_created')
#     paginator = Paginator(all_posts, 10)
#     page_number = request.GET.get('page')
#     if page_number == None:
#         page_number = 1
#     posts = paginator.get_page(page_number)
#     followings = []
#     suggestions = []
#     if request.user.is_authenticated:
#         followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
#         suggestions = Author.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
#     return render(request, "index.html", {
#         "posts": posts,
#         "suggestions": suggestions,
#         "page": "all_posts",
#         'profile': False
#     })
def homeView(request):
    all_posts = POST.objects.all().order_by('-published')
    followings = []
    suggestions = []
    if request.user.is_authenticated:
        # followings = Follower.objects.filter(follower=request.user).values_list('user', flat=True)
        suggestions = Author.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]

    template_name = '../frontend/index.html'
    return render(request, template_name, {
        "posts": all_posts,
        "suggestions": suggestions,
        "page": "all_posts",
        'profile': False
    }
    )

def loginView(request):
    template_name = 'author/login.html'
    serializer_class = LoginSerializer
    
    if request.method == 'POST':

        # serializer = serializer_class(data=request.data,
        #                                    context={'request': request})
        # serializer.is_valid(raise_exception=True)
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)

        user = authenticate(request, username = username, password = password)

        print(user)
        
        if user:
            print("yesssssss")
            if not user.is_active:
                # print("This is NOT an active user.")
                messages.error(request, 'Account Activation Pending.', extra_tags='inactive')
                return HttpResponse(render(request, 'author/login.html'),status=401)
            else:
                login(request, user)
            return redirect(homeView)
            return HttpResponse(render(request, 'author/home.html'),status=200)

        else:
            messages.error(request, 'Please enter a valid username and password. Note that both fields are case sensitive.', extra_tags='invalid')
            return HttpResponse(render(request, 'author/login.html'),status=401)
        

    return render(request, template_name)

def registerView(request):
    
    template_name = 'author/register.html'
    form = CreateAuthorForm()

    serializer_class = AuthorRegisterSerializer

    if request.method == 'POST':
        form = CreateAuthorForm(request.POST)
        
        if form.is_valid():
            git_user = form.cleaned_data.get('github')
            github_url = f'http://github.com/{git_user}'
            user = Author.objects.create_user(displayName=form.cleaned_data.get('displayName'), username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'), github=github_url)

            return redirect(loginView)
            #return HttpResponseRedirect('/login')

    context = {'form':form}
    return render(request, template_name, context)

def logoutView(request):
    logout(request)
    messages.success(request, ("You were logged out"))
    return redirect(loginView)

    