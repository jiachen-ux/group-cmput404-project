from django.urls import path 
from . import views
from .viewsets import LoginViewSet, RefreshTokenViewSet
from rest_framework_nested import routers



router = routers.SimpleRouter()
router.register(r'login', LoginViewSet, basename='auth_login')
router.register(r'refresh', RefreshTokenViewSet, basename='auth_refresh')
urlpatterns = [
    path('register/', views.AuthorCreate.as_view()),
    path('data/', views.testAuth),

    path('authors/', views.getAllAuthors, name="allForeignAuthors"), # TODO add pagination
    path('authors/<id>/', views.foreignUser, name="singleForeignAuthor"),

    path('author/search/', views.AuthorSearchView.as_view()), 
    path("logout", views.logoutView, name="logout_url"),
    *router.urls,
]