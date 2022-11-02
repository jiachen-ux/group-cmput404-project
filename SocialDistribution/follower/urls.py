from django.urls import URLPattern, path 

from follower.views import(
    send_follow_request
)

app_name = "follower"

urlpatterns = [
    path('follow_request/', send_follow_request, name="follow-request"),
]
