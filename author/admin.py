from django.contrib import admin
from . import models 

admin.site.register(models.Author)
admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.Follower)
# Register your models here.
