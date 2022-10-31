from django.contrib import admin
from django.dispatch import receiver

from follower.models import Follower, FollowRequest

# Register your models here.

class FollowerAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = Follower

admin.site.register(Follower, FollowerAdmin)

class FollowRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'reciever']
    list_display = ['sender', 'reciever']
    search_fields = ['sender__username', 'sender__email','reciever__username', 'receiver__email']
   

    class Meta:
        model = FollowRequest

admin.site.register(FollowRequest, FollowRequestAdmin)


    


