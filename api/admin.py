from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from api import models


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', )
    search_fields = ['user__email', 'user__username', 'user__first_name', 'user__last_name']

class EventResource(resources.ModelResource):
    class Meta:
        model = models.Event

class EventAdmin(ImportExportModelAdmin):
    resource_class = EventResource
    search_fields = [
        'title',
        'description',
        'codeweek_for_all_participation_code',
        'creator__email',
        'creator__username',
        'creator__first_name',
        'creator__last_name',
    ]
    prepopulated_fields = {'slug': ('title',)}
    list_display = (
        'title',
        'status',
        'location',
        'country',
        'start_date',
        'reported_at',
        'participants_count',
        'average_participant_age',
        'percentage_of_females',
    )
    list_editable = ('status',)
    list_filter = ('status', 'start_date')
    filter_horizontal = ('audience',)
    filter_horizontal = ('theme',)

admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.events.EventAudience)
admin.site.register(models.events.EventTheme)
