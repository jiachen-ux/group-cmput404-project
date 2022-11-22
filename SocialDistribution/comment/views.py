from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json

from .models import *
from follower.models import Follower
from post.models import Post
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
# Create your views here.

@api_view(['POST','GET'])
@csrf_exempt
def comment(request, postid):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = json.loads(request.body)
            comment = data.get('comment_text')
            post = Post.objects.get(id=postid)
            try:
                newcomment = Comment.objects.create(post=post,commenter=request.user,comment_content=comment)
                post.comment_count += 1
                post.save()
                print(newcomment.to_dict())
                return JsonResponse([newcomment.to_dict()], safe=False, status=201)
            except Exception as e:
                return HttpResponse(e)
    
        post = Post.objects.get(id=postid)
        comments = Comment.objects.filter(post=post)
        comments = comments.order_by('-comment_time').all()
        return JsonResponse([comment.to_dict() for comment in comments], safe=False)
    else:
        return HttpResponseRedirect(reverse('login'))