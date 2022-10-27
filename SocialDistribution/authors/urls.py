from django.urls import path
from .views import AuthorView

from django.contrib import admin
from django.urls import path


from .views import index, post_list_view , post_create_view #post_delete_view,post_detail_view


urlpatterns = [
    path('author', AuthorView.as_view()),
    path('', index),
    #path('front',index),
    path('posts', post_list_view),
    path('create-post', post_create_view),
    #path('posts/<int:post_id>', post_detail_view),
    #path('api/posts/<int:post_id>/delete', post_delete_view), 
]
 