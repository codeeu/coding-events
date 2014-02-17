from django.contrib import admin

from api import models
#from api.models import events


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', )


admin.site.register(models.UserProfile, UserProfileAdmin)
