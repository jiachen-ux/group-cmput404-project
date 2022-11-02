from django.http import HttpResponse
import json
from author.models import Author
from follower.models import FollowRequest



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


                



