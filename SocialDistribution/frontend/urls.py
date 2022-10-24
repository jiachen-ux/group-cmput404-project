
from django.urls import path

from .views import index, post_list_view , post_create_view

urlpatterns = [
    path('', index),
    path('front',index),
    path('posts', post_list_view),
    path('createpost', post_create_view)  

]