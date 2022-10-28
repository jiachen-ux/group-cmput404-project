<<<<<<< HEAD
<<<<<<< HEAD:author/urls.py
 
from django.urls import path
from . import views

urlpatterns = [
    path('register/',  views.AuthorCreateView.as_view()),
=======
=======
>>>>>>> parent of 407ea186 (new)
from django.urls import path
from .views import AuthorView

urlpatterns = [
    path('author', AuthorView.as_view()),
<<<<<<< HEAD
>>>>>>> parent of 407ea186 (new):SocialDistribution/authors/urls.py
=======
>>>>>>> parent of 407ea186 (new)
]
