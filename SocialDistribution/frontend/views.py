from turtle import pos
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import Post
import random
from .forms import PostForm
def index(request, *args, **kwargs):
   #return render(request, 'frontend/index.html')
    return render(request, "pages/home.html", context={},status=200)

def post_create_view(request, *args, **kwargs):
    form = PostForm(request.POST or None)#send data or none
    if form.is_valid(): #if valid
        obj = form.save(commit=False)
        #do other logic 
        obj.save()
        form = PostForm()
    return render(request, 'templates/components/forms.html', context={"form": form}) #if not valid

def post_list_view(request, *args, **kwargs):
    qs = Post.objects.all() #list
    post_list = [{"id": x.id, "content":x.content, "likes": random.randint(0, 10)} for x in qs]
    data = {
        "isUser": False,
        "response": post_list 
    }
    return JsonResponse(data) 