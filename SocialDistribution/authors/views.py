# Create your views here.
import imp
from django.dispatch import receiver
from django.shortcuts import  render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from follower.follower_status import FollowRequestStatus

from .forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import generics, response, status
from rest_framework.response import Response
from .models import Author 
from .serializers import AuthorSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from follower.utils import get_follow_request_or_false
from follower.models import Follower,FollowRequest


class AuthorView(generics.RetrieveAPIView):
    # https://www.django-rest-framework.org/api-guide/generic-views/ for reference
    serializer_class = AuthorSerializer
    http_method_names = ['get', 'put']
    lookup_field = 'userId'

    # Override get_queryset() https://www.django-rest-framework.org/api-guide/generic-views/#get_querysetself
    def get_queryset(self):
        id = self.kwargs['userId']
        return Author.objects.filter(userId=id)
    
    
class AuthorListView (generics.ListAPIView):
    # get all authors in local server
    http_method_names = ['get']
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
    def list(self):
        try:
            serializer = AuthorSerializer(self.queryset, many=True)
            return Response({"type": 'authors',"items":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error: {e}", status=status.HTTP_404_NOT_FOUND)
    
    
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
                return redirect("/home") 
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


def home(request):
    return render (request, 'authors/home.html', {})


@login_required
def display_author_profile(request, user_id):
    author = User.objects.get(pk=user_id)

    try:
        friend_list = Follower.objects.get(user=author)
    except Follower.DoesNotExist:
        friend_list = Follower(user=author)
        friend_list.save()

    friends = friend_list.friends.all()
    context['friends'] = friends

    is_self = True
    is_friend = False
    user = request.user
    request_sent= FollowRequestStatus.NO_REQUEST_SENT.value
    friend_request = None

    if user.is_authenticated and user != author:
        is_self = False
        if friends.filter(pk=user.id):
            is_friend = True
        else:
            is_friend = False
            # CASE1: request has been sent to you
            if get_follow_request_or_false(sender=author, reciever=user) != False:
                request_sent = FollowRequestStatus.THEY_SENT_YOU.value
                context['pending_friend_request_id'] = get_follow_request_or_false(sender=author, reciever=user).id

            # CASE 2: request has been sent to them from you
            elif get_follow_request_or_false(sender=author, reciever=user) != False:
                request_sent = FollowRequestStatus.YOU_SENT_THEM.value

            #case 3: no request sent 
            else:
                request_sent = FollowRequestStatus.NO_REQUEST_SENT.values


    elif not user.is_authenticated:
        is_self = False
    
    else:
        try:
            friend_request = FollowRequest.objects.filter(receiver=user, is_active=True)
        except:
            pass

    context['is_self'] = is_self
    context['is_friend'] = is_friend
    context['request_sent'] = request_sent
    context['friend_request'] = friend_request

    context = {
        "author":author
    }
    return render(request, 'authors/profile.html', context) 

@login_required
def searched_author(request):
    # assume author exist and user name is correct
    #username = request.GET['username']
    #author = Author.objects.get(username=username)
    #id = author.userId

    if request.method == "POST":
        q = request.POST['q']
        results = User.objects.filter(username__contains = q)
    
        return render(request, 'authors/listUsers.html', {'q':  q, 'results':results})
    
    else:
        results = User.objects.all()
        return render(request, 'authors/listUsers.html', {'results':results})
