from django.contrib import admin

from api import models


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', )


class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'status', 'location', 'country', 'start_date')
    list_editable = ('status',)
    list_filter = ('status', 'start_date')
    filter_horizontal = ('audience',)
    filter_horizontal = ('theme',)

admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.events.EventAudience)
admin.site.register(models.events.EventTheme)
