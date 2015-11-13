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

class IsReportedAtListFilter(admin.SimpleListFilter):
    title = u'reported state'
    parameter_name = u'reported'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Reported'),
            ('0', 'Not reported'),
        )

    def queryset(self, request, queryset):
        kwargs = {'reported_at': None}

        if self.value() == '0':
            return queryset.filter(**kwargs)
        if self.value() == '1':
            return queryset.exclude(**kwargs)

        return queryset

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
    list_filter = ('status', 'start_date', IsReportedAtListFilter, 'last_report_notification_sent_at', 'report_notifications_count')
    filter_horizontal = ('audience',)
    filter_horizontal = ('theme',)

admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.events.EventAudience)
admin.site.register(models.events.EventTheme)
