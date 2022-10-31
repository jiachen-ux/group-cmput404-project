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
from django.urls import path
from author import views as author_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", author_views.login_view, name="login"),
    # path("logout/", author_views.logout_view, name="logout"),
    path("home", author_views.home),
    path("search", author_views.searched_author, name='search'),
    path("register/", author_views.register, name="register"),
    path('profile/<user_id>', author_views.display_author_profile, name='view-profile'),
]
