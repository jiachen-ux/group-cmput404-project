from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


from . import views

urlpatterns = [
     # Comment routes!
    path('authors/<uuid:uuidOfAuthor>/posts/<postId>/comments', views.commentDetails),
    path("comment/", views.commentDetails),
    path("posts/<postId>/comments", views.commentDetails, name="view-comment")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)