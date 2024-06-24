from django.contrib import admin

from profiles_api import models

# Register your models here.
admin.site.register(models.UserProfile) #to register models with admin site to be accessible through admin interface
