from django.dispatch import receiver
from django.shortcuts import render
from django.http import HttpResponse
import json

from authors.models import Author
from follower.models import FollowRequest



# Create your views here.

def send_friend_request(request):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id =  request.POST.get("reciever_user_id")
        if user_id:
            receiver = Author.objects.get(pk=user_id)
            try:
                # get any friend requests (active and non-active)
                friend_request = FollowRequest.objects.filter(sender=user, receiver=receiver)

                #find is any of them are active
                try:
                    for request in friend_request:
                        if request.is_active:
                            raise Exception("Yoy already sent them a friend request.")

                    friend_request =  FollowRequest(sender=user, receiver=receiver)
                    friend_request.save()
                    payload['response'] = 'Friend request sent.'
                except Exception as e:
                    payload['response'] = str(e)
            except FollowRequest.DoesNotExist:
                # there are no friend requests so create one.

                friend_request = FollowRequest(sender=user, receiver=receiver)
                friend_request.save()
                payload['response'] = 'Friend request sent.'

            if payload['response'] == None:
                payload['response'] = "Something went wrong."
        else:
            payload['response'] = "Unable to send a friend request."
    else:
         payload['response'] = "You must be authenticated to send friend request"

    return HttpResponse(json.dumps(payload), content_type="application/json")


                



