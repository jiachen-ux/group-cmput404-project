from functools import partial
import json
from re import A
import re
from . import utils
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from rest_framework import generics, mixins, response, status
import requests
from requests.auth import HTTPBasicAuth
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
from author.serializers import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from post.models import Post
from author.forms import EditAuthorForm

# from connect.views import *
# from connect.models import *


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


class AuthorAPIView(generics.ListAPIView):

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

@login_required
def homeView(request):
    template_name = 'author/home.html'
    return render(request, template_name)

def loginView(request):
    template_name = 'author/login.html'
    serializer_class = LoginSerializer

    
    if request.method == 'POST':

        # serializer = serializer_class(data=request.data,
        #                                    context={'request': request})
        # serializer.is_valid(raise_exception=True)

        
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username)
        # print(password)

        user = authenticate(request, username = username, password = password)

        # print(user)

        
        if user:
            # print("yesssssss")
            if not user.is_active:
                # print("This is NOT an active user.")
                messages.error(request, 'Account Activation Pending.', extra_tags='inactive')
                return HttpResponse(render(request, 'author/login.html'),status=401)
            else:
                login(request, user)
            # return redirect(homeView)
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


def get_local_remote_author(request):
    '''
    get all authors, local and remote and show them in browser
    '''
    team8 = 'https://c404-team8.herokuapp.com/api/'
    team7 = 'https://cmput404-social.herokuapp.com/service/'

    local_Authors = Author.objects.all()
    serializer = GetAuthorSerializer(local_Authors, many=True)
    a = json.dumps(serializer.data)
    local_authors_data = json.loads(a)
    # print(local_authors_data)
    team8_remote_response = requests.get(f'{team8}authors/')
    team7_remote_response = requests.get(f'{team7}authors/')
    combined_author = []

    for author in local_authors_data:
        author['id'] = author['id'].split('/')[-1]
    combined_author.extend(local_authors_data)

    if team8_remote_response.status_code == 200: 
        # print('connect to team 8')
        team8_data = team8_remote_response.json()
        team8_Authors = team8_data['items']
        combined_author.extend(team8_Authors)
    
    if team7_remote_response.status_code == 200:
        # print('connect to team 7')
        team7_data = team7_remote_response.json()
        team7_Authors = team7_data['items']
        combined_author.extend(team7_Authors)
    return combined_author


@login_required
def profile(request, authorId):
    # # get user's information
    # team8_remote_response = requests.get(f'{team8}authors/')
    # team7_remote_response = requests.get(f'{team7}authors/')        
    # if team8_remote_response.status_code == 200:
    #     print('connect to team 8')
    #     team8_data = team8_remote_response.json()
    #     team8_Authors = team8_data['items']
    #     combined_author.extend(team8_Authors)
    
    # if team7_remote_response.status_code == 200:
    #     print('connect to team 7')
    #     team7_data = team7_remote_response.json()
    #     team7_Authors = team7_data['items']
    #     combined_author.extend(team7_Authors)
    authors = get_local_remote_author(request)
    team8 = 'https://c404-team8.herokuapp.com/api/'
    team7 = 'https://cmput404-social.herokuapp.com/service/'
    display_name = ''
    github_url = ''
    posts = []
    host = ''
    id=''
    profile_image = ''
    is_self = True
    user = request.user

    # try:
    #     current_author = get_object_or_404(Author, id = authorId)
    # except Author.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)

    for author in authors:
        # print(author)
        if authorId == author['id']: #or authorId== author['id'].split('/')[-1]:
            print('found it')
            display_name = author['displayName']
            github_url = author['github']
            host = author['host']
            id= author['id']
            profile_image = author['profileImage']
            break
            
    if host in team8:
        # print('connect tean 8')
        response = requests.get(f"{team8}authors/{authorId}/posts/",
                                params=request.GET)
        if response.status_code == 200:
            posts = response.json()['items']

    elif host in team7:
        # print('connect tean 7')
        response = requests.get(f"{team7}authors/{authorId}/posts/",
                                params=request.GET)
        if response.status_code == 200:
            posts = response.json()['items']
    else:
        posts = Post.objects.filter(author__id=authorId, visibility="PUBLIC", unlisted=False)

    if user.is_authenticated and str(user.id) != authorId:
            is_self = False
    

    context = {
        'displayName': display_name,
        'github_url': github_url,
        'posts': posts,
        'id':id,
        'is_self': is_self,
        'profileImage': profile_image
    }


    print(context['is_self'])

    # print(context)
    return render(request, 'author/profile.html', context)


def display_author(request):
    authors = get_local_remote_author(request)
    context = {
        "type": "authors",
        "items": authors
    }
    
    # for result in combined_author:
    #     print(result)
    # print(context['items'])
    # return response.Response(context,status=status.HTTP_200_OK)
    return HttpResponse(render(request, 'author/listUsers.html', context),status=200)


def profileEdit(request):

    authorId = request.user.id
    print(authorId)

    if request.method == "POST":
        form = EditAuthorForm(request.POST, instance=request.user)

        if form.is_valid():
            github_username = form.cleaned_data['github']
            displayName = form.cleaned_data['displayName']
            username = form.cleaned_data['username']
            
            request.user.github = "http://github.com/" + github_username
            request.user.displayName = displayName
            request.user.username = username
            

            form.save()
            messages.success(request, 'Profile updated successfully.', extra_tags='success')
            return redirect(display_author)
        else:
            messages.success(request, 'Profile could not be updated.', extra_tags='failure')
            return redirect(display_author)
    else:
        form = EditAuthorForm(instance=request.user)
        git_url = request.user.github
        displayName = request.user.displayName
        username = request.user.username

        gituser = git_url.replace("http://github.com/", "")
        context = {'form':form, 'github_username':gituser, 'displayName':displayName, 'username':username, 'id':authorId}
        
        return HttpResponse(render(request, 'author/editProfile.html', context),status=200)
        #return render(request, 'author/editProfile.html', context)

    

