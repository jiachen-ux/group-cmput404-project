from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("authors/login", views.login_view, name="login"),
    path("authors/logout", views.logout_view, name="logout"),
    path("authors/register", views.register, name="register"),
    path("<uuid:userid>", views.profile, name='profile')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)