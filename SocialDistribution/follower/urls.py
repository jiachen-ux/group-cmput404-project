from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path("authors/following", views.following, name='following'),
    path("service/authors/<userid>/follow", views.follow, name="followuser"),
    path("service/authors/<userid>/unfollow", views.unfollow, name="unfollowuser")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

