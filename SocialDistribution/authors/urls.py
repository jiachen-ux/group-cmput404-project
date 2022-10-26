from django.urls import path
from .views import AuthorListView

urlpatterns = [
    path('author', AuthorListView.as_view()),
]
