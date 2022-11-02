from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework.response import Response
from .forms import UserRegisterForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rest_framework import status

from .models import Author
from follower.models import Follower
from post.models import Post

# Create your views here.
def login_view(request):
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
                messages.info(request,"Invalid username or password.")
        else:
            messages.info(request,"Invalid username or password.")
    form = AuthenticationForm()
    context = {"login_form":form}
    return render(request, "author/login.html", context)


# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful." )
            return redirect('/login')
        messages.info(request, "Unsuccessful registration. Invalid information.")

    form = UserRegisterForm()
    context = {'register_form': form}

    return render(request, 'author/register.html', context)



def profile(request, username):
    user = Author.objects.get(username=username)  
    all_posts = Post.objects.filter(author=user).order_by('-date_created')
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
        suggestions = Author.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]

        if request.user in Follower.objects.get(user=user).followers.all():
            follower = True
    
    follower_count = Follower.objects.get(user=user).followers.all().count()
    following_count = Follower.objects.filter(followers=user).count()
    return render(request, 'author/profile.html', {
        "username": user,
        "posts": posts,
        "posts_count": all_posts.count(),
        "suggestions": suggestions,
        "page": "profile",
        "is_follower": follower,
        "follower_count": follower_count,
        "following_count": following_count
    })

@login_required
def display_author_profile(request, userId):
    try:
        author = get_object_or_404(Author, userId = userId)

    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    context = {
        "author":author
    }
    return render(request, 'author/profile.html', context) 

def check(request):
    # get author's info
    
    return render(request, 'author/profile.html', {}) 
    

@login_required
def searched_author(request):
    # assume author exist and user name is correct
    #username = request.GET['username']
    #author = Author.objects.get(username=username)
    #id = author.userId

    if request.method == "POST":
        q = request.POST['q']
        results = Author.objects.filter(username__contains = q)
        print(results)
        return render(request, 'author/listUsers.html', {'q':  q, 'results':results})
    
    else:
        results = Author.objects.all()
        return render(request, 'author/listUsers.html', {'results':results})