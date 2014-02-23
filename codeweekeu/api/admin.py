from django.contrib import admin

from api import models


class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'country', )


class EventAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	list_display = ('title', 'status')
	list_editable = ('status',)
	list_filter = ('status', 'start_date')

admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Event, EventAdmin)