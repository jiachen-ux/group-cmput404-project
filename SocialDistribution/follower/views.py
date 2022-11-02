from django.http import HttpResponse
import json
from author.models import Author
from follower.models import FollowRequest
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import *
from post.models import Post



# Create your views here.

def send_follow_request(request):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        userid =  request.POST.get("receiver_userid")
        print("userid: "+userid)
        
        if userid:
            print ("if userid")
            reciever = Author.objects.get(userid=userid)
            print("reciever: ")
            print(reciever)
            print("user: ")
            print(user)

            try:
                # get any follow requests (active and non-active)
                print ("in")
                follow_request = FollowRequest.objects.filter(sender=user, reciever=reciever)
                print(follow_request)

                #find is any of them are active
                try:
                    for request in follow_request:
                        if request.is_active:
                            raise Exception("Yoy already sent them a follow request.")

                    follow_request =  FollowRequest(sender=user, reciever=reciever)
                    follow_request.save()
                    payload['response'] = 'Follow request sent.'
                except Exception as e:
                    payload['response'] = str(e)
            except FollowRequest.DoesNotExist:
                # there are no follow requests so create one.

                follow_request = FollowRequest(sender=user, reciever=reciever)
                follow_request.save()
                payload['response'] = 'Follow request sent.'

            if payload['response'] == None:
                payload['response'] = "Something went wrong."
        else:
            payload['response'] = "Unable to send a follow request."
    else:
         payload['response'] = "You must be authenticated to send follow request"

    return HttpResponse(json.dumps(payload), content_type="application/json")


            

def following(request):
    if request.user.is_authenticated:
        following_user = Follower.objects.filter(followers=request.user).values('user')
        all_posts = Post.objects.filter(creater__in=following_user).order_by('-date_created')
        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page')
        if page_number == None:
            page_number = 1
        posts = paginator.get_page(page_number)
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = Author.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        return render(request, "index.html", {
            "posts": posts,
            "suggestions": suggestions,
            "page": "following"
        })
    else:
        return HttpResponseRedirect(reverse('login'))
@csrf_exempt
def follow(request, username):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            user = Author.objects.get(username=username)
            print(f".....................User: {user}......................")
            print(f".....................Follower: {request.user}......................")
            try:
                (follower, create) = Follower.objects.get_or_create(user=user)
                follower.followers.add(request.user)
                follower.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def unfollow(request, username):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            user = Author.objects.get(username=username)
            print(f".....................User: {user}......................")
            print(f".....................Unfollower: {request.user}......................")
            try:
                follower = Follower.objects.get(user=user)
                follower.followers.remove(request.user)
                follower.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))
