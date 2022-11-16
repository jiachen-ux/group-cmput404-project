from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path("authors/following", views.following, name='following'),
    path("<uuid:userid>/follow", views.follow, name="followuser"),
    path("<uuid:userid>/unfollow", views.unfollow, name="unfollowuser")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

