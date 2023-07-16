from django.contrib import admin
from profiles_api import models
# Register your models here.

# enable admin to use the models
admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)