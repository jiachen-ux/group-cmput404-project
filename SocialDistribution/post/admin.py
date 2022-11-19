from django.contrib import admin
from . import models


admin.site.register(models.POST)
admin.site.register(models.Like)
admin.site.register(models.Inbox)