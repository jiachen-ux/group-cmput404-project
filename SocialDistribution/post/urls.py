from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
urlpatterns = [
    path("service/authors/post", views.create_post, name="createpost"),
    path("service/authors/post/<uuid:id>/like", views.like_post, name="likepost"),
    path("service/authors/post/<uuid:id>/unlike", views.unlike_post, name="unlikepost"),
    path("service/authors/post/<uuid:post_id>/delete", views.delete_post, name="deletepost"),
    path("service/authors/post/<uuid:post_id>/edit", views.edit_post, name="editpost")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)