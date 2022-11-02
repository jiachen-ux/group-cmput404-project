from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("n/login", views.login_view, name="login"),
    path("n/logout", views.logout_view, name="logout"),
    path("n/register", views.register, name="register"),
    path("<slug:username>", views.profile, name='profile')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)