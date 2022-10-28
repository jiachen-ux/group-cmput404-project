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
from django.urls import path, include
<<<<<<< HEAD
<<<<<<< HEAD:SocialDist/urls.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('author.urls'))
=======
=======
>>>>>>> parent of 407ea186 (new)
from authors import views as author_view
from post import views as post_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("register", author_view.register_page),
    path("login", author_view.login_page),
    path("posts/", post_view.PostApiView.as_view(), name="posts-list"),
    path("author/<str:author_id>/posts/", post_view.PostApiView.as_view(), name="author-posts"),
    path("author/<str:author_id>/posts/<str:post_id>", post_view.PostApiView.as_view(), name="post-detail"),
    path('', include('frontend.urls')),
    path('', include('authors.urls'))
<<<<<<< HEAD
>>>>>>> parent of 407ea186 (new):SocialDistribution/SocialDistribution/urls.py
=======
>>>>>>> parent of 407ea186 (new)
]
