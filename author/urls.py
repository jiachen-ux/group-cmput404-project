 
from django.urls import path
from . import views

urlpatterns = [
    path('register/',  views.AuthorCreateView.as_view()),
]
