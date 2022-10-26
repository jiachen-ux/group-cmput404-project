# Create your views here.
from django.shortcuts import  render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import generics, response, status
from rest_framework.response import Response
from .models import Author 
from .serializers import AuthorSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from SocialDistribution.authors import serializers

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
                # return redirect("authors:profile") <- this should redirect to a page that show's user's main page
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


@login_required
def display_author_profile(request, userId):
    # get author's info
    author = get_object_or_404(Author, userId = userId)
    context = {
        "author":author
    }
    return render(request, 'profile.html', context)
    
    


@login_required
def get_author(request):
    # assume author exist and user name is correct
    username = request.GET['username']
    author = Author.objects.get(username=username)
    id = author.userId
    return redirect('author:profile', userId=id)
    

