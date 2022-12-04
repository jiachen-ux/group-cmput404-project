from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
  # Follower routes!
    # path('authors/<uuid:uuidOfAuthor>/followers', views.getAllFollowers),
    # path('authors/<uuid:authorID>/followers/<uuid:foreignAuthor>', views.handleSingleFollow),

    # # Follow Request routes! (This is not specified in the description)
    # path('authors/<uuid:sender>/followrequest/<uuid:receiver>', views.handleFollowRequest), 
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

