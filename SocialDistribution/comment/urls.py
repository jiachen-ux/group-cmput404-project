from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
urlpatterns = [
    path("n/post/<int:post_id>/comments", views.comment, name="comments"),
    path("n/post/<int:post_id>/write_comment",views.comment, name="writecomment")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)