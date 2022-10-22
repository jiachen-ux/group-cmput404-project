# Create your views here.
from django.shortcuts import  render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm

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