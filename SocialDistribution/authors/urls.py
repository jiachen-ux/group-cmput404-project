from django.urls import path
from . import views

urlpatterns = [
    path('register/',  views.register_page.as_view()),
    path('author', views.AuthorView.as_view()),
]
