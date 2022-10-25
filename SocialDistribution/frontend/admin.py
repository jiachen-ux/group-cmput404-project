from django.contrib import admin

# Register your models here.
from .models import Post, Like

class PostLikeAdmin(admin.TabularInline):
    model = Like

class PostAdmin(admin.ModelAdmin):
    inlines = [PostLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['content', 'user__username', 'user__email'] # only allow searches about content, username and email
    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)