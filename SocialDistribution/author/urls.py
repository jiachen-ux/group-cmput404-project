from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("service/authors/login", views.login_view, name="login"),
    path("service/authors/logout", views.logout_view, name="logout"),
    path("service/authors/register", views.register, name="register"),
    path("service/auhtors/<uuid:userid>", views.profile, name='profile'),
    path("service/authors/", views.ProfileView.as_view(), name='all-profiles'),
    path("service/authors/<uuid:uuid>", views.SingleProfileView.as_view(), name='Single-profile')

    # path("auth/", include('djoser.urls')),
    # path("auth/", include('djoser.urls.authtoken')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)