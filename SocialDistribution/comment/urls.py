from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
urlpatterns = [
     # Comment routes!
    path('authors/<uuid:uuidOfAuthor>/posts/<uuid:uuidOfPost>/comments', views.CommentPostView.as_view()),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)