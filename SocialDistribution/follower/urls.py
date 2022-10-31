from django.urls import URLPattern, path 

from follower.views import(
    send_friend_request
)

app_name = "follower"

urlpatterns = [
    path('friend_request/', send_friend_request, name="friend-request"),
]