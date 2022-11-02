from follower.models import FollowRequest

def get_follow_request_or_false(sender, reciever):

    try:
        return FollowRequest.objects.get(sender=sender, reciever=reciever, is_active=True)
    
    except FollowRequest.DoesNotExist:
        return False

