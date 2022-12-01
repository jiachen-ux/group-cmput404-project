"""SocialDistribution URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
import author.views as author_view
import post.views as post_view
import follower.views as follower_view
import comment.views as comment_view


schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Posts API",
        default_version='1.0.0',
        description="API documentation of App",
    ),
    public=True,
)

urlpatterns = [
    path("register/", author_view.registerView, name="register_url"),
    path("", author_view.loginView, name="login_url"),


    path("home/", author_view.homeView),
    path("admin/", admin.site.urls),
    path('authors/<authorId>/', author_view.profile, name="author_profile"),
    path('authors/', author_view.display_author, name="allForeignAuthors"),

    # path("", include("author.urls")),
    path("", include("comment.urls")),
    path("", include("post.urls")),
    path("", include("follower.urls")),

    # api
    # authors
    path('service/authors/', author_view.getAllAuthors),

    # single author
    path('service/authors/<uuid:uuidOfAuthor>', author_view.getSingleAuthor),
    
    # followers
    # all followers
    path('service/authors/<uuid:uuidOfAuthor>/followers', follower_view.getAllFollowers),
    # follower request
    path('service/authors/<uuid:sender>/followrequest/<uuid:receiver>', follower_view.handleFollowRequest),
    path('service/authors/<uuid:authorID>/followers/<uuid:foreignAuthor>', follower_view.handleSingleFollow),
    # post
    path('service/authors/<uuid:uuidOfAuthor>/posts/<uuid:uuidOfPost>/', post_view.PostSingleDetailView.as_view()),
    # get all public posts
    path("service/authors/<uuid:uuidOfAuthor>/posts/getallpublicpost", post_view.PostAllPublicPost.as_view()),
 
    # get all post
    path('service/authors/<uuid:uuidOfAuthor>/posts/', post_view.PostMutipleDetailView.as_view()),

    # TODO: Image posts
    
    # comments
    path('service/authors/<uuid:uuidOfAuthor>/posts/<uuid:uuidOfPost>/comments', comment_view.CommentPostView.as_view()),
    path('service/authors/<uuid:uuidOfAuthor>/posts/<uuid:uuidOfPost>/comments/<uuid:uuidOfComment>/likes', post_view.getAllCommentLikes),

    # likes
    path('service/authors/<uuid:uuidOfAuthor>/posts/<uuid:uuidOfPost>/likes', post_view.PostLike.as_view()),

    # Liked routes!
    path('service/authors/<uuid:uuidOfAuthor>/liked', post_view.getAllAuthorLiked),

    # Inbox routes!
    path("service/authors/<uuid:author_id>/inbox", post_view.handleInboxRequests),
    # Inbox route to get everything (not only posts!)
    path("service/authors/<uuid:author_id>/inboxAll", post_view.getEntireInboxRequests),

    path('swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
]
