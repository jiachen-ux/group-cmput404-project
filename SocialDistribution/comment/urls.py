from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
urlpatterns = [
    path("authors/post/<uuid:postid>/comments", views.comment, name="comments"),
    path("authors/post/<uuid:postid>/write_comment",views.comment, name="writecomment")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)