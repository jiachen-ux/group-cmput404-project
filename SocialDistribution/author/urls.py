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

    # path('authors/', views.getAllAuthors), # TODO add pagination
    path('authors/<authorId>/', views.profile, name="author_profile"),


    path('authors/edit/', views.profileEdit, name="editProfile"),

    path('authors/', views.display_author, name="allForeignAuthors"),

    path('author/search/', views.AuthorSearchView.as_view()), 
    path("logout", views.logoutView, name="logout_url"),
    *router.urls,
]