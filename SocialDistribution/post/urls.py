from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
app_name = 'post'
urlpatterns = [
    #    # Post routes!
    # path('authors/<uuid:uuidOfAuthor>/posts/<uuid:uuidOfPost>/', views.PostSingleDetailView.as_view()),
    # path('authors/<uuid:uuidOfAuthor>/posts/', views.PostMutipleDetailView.as_view()),
    # path("authors/<uuid:uuidOfAuthor>/posts/getallpublicpost", views.PostAllPublicPost.as_view()),
 

    # Like routes!
    # path('authors/<uuid:uuidOfAuthor>/posts/<uuid:uuidOfPost>/likes', views.PostLike.as_view()),
    # path('authors/<uuid:uuidOfAuthor>/posts/<uuid:uuidOfPost>/comments/<uuid:uuidOfComment>/likes', views.getAllCommentLikes),
    # path('authors/<uuid:uuidOfAuthor>/posts/<uuid:uuidOfPost>/getalllikes', views.getAllPostLikes.as_view()),

    # # Liked routes!
    # path('authors/<uuid:uuidOfAuthor>/liked', views.getAllAuthorLiked),
    
    # # Inbox routes!
    # path("authors/<uuid:author_id>/inbox", views.handleInboxRequests),

    # # Inbox route to get everything (not only posts!)
    # path("authors/<uuid:author_id>/inboxAll", views.getEntireInboxRequests),

    path('site/posts', views.postIndex, name='index'),
    path('site/my_posts', views.myPosts, name='myPosts'),
    path('site/inboxs', views.Inboxs, name='inboxs'),
    path('site/foreign_posts', views.getForeignPosts, name='foreignPosts'),
    path('createpost',views.createpost,name='createpost'),
    path('editpost/<str:post_id>',views.editpost, name='editpost'),
    path('deletepost/<str:post_id>',views.deletepost, name='deletepost'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)