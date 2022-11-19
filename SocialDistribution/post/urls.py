from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
urlpatterns = [
       # Post routes!
    path('authors/<uuid:uuidOfAuthor>/posts/<uuid:uuidOfPost>/', views.PostSingleDetailView.as_view()),
 

    # Like routes!
    path('authors/<uuid:uuidOfAuthor>/posts/<uuid:uuidOfPost>/likes', views.getAllPostLikes),
    path('authors/<uuid:uuidOfAuthor>/posts/<uuid:uuidOfPost>/comments/<uuid:uuidOfComment>/likes', views.getAllCommentLikes),

    # Liked routes!
    path('authors/<uuid:uuidOfAuthor>/liked', views.getAllAuthorLiked),
    
    # Inbox routes!
    path("authors/<uuid:author_id>/inbox", views.handleInboxRequests),

    # Inbox route to get everything (not only posts!)
    path("authors/<uuid:author_id>/inboxAll", views.getEntireInboxRequests),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)