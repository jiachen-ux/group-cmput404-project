<<<<<<< Updated upstream
from django.urls import URLPattern, path 

from follower.views import(
    send_follow_request
)

app_name = "follower"

urlpatterns = [
    path('follow_request/', send_follow_request, name="follow-request"),
]
=======
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path("n/following", views.following, name='following'),
    path("<slug:username>/follow", views.follow, name="followuser"),
    path("<slug:username>/unfollow", views.unfollow, name="unfollowuser")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> Stashed changes