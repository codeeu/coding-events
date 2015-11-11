from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import Q

from api.processors import events_pending_for_report
from api.processors import events_pending_for_report_for
from api.models.users import User
from mailer.event_report_mailer import send_reminder_for_event_report_and_certificate

class Command(BaseCommand):
    help = 'Sends a notification email to each organizer with unreported events. Only a limited number of emails is sent per run. Should be run via a cron each hour.'

    def handle(self, *args, **options):
        emails_per_hour = settings.EVENT_REPORT_REMINDER_EMAILS_PER_HOUR
        max_reminders   = settings.EVENT_REPORT_REMINDERS_LIMIT
        remind_interval = settings.EVENT_REPORT_REMINDERS_INTERVAL_IN_DAYS
        from_email      = settings.EVENT_REPORT_REMINDERS_FROM_EMAIL

        last_reminder_sent_before = datetime.now() - timedelta(days=remind_interval)

        events_to_report = events_pending_for_report().filter(
                Q(last_report_notification_sent_at=None) |
                Q(last_report_notification_sent_at__lte=last_reminder_sent_before)
            ).filter(
                report_notifications_count__lt=max_reminders
            )

        organizer_ids = events_to_report.distinct().values_list('creator_id', flat=True)
        organizers = User.objects.filter(id__in=organizer_ids)

        self.stdout.write(
            'We have to notify {organizers_count} organizer(s) in a total of {events_count} event(s)'.format(
                events_count=events_to_report.count(),
                organizers_count=organizers.count()
            )
        )

        for organizer in organizers[:emails_per_hour]:
            unreported_organizer_events = events_pending_for_report_for(organizer)
            unrepored_events_count = unreported_organizer_events.count()

            self.stdout.write(
                'Emailing {contact} for {events_count} unreported event(s)'.format(
                    contact=organizer.email_with_name(),
                    events_count=unrepored_events_count
                )
            )

            send_reminder_for_event_report_and_certificate(organizer, unrepored_events_count)

            for event in unreported_organizer_events:
                event.last_report_notification_sent_at = datetime.now()
                event.report_notifications_count += 1
                event.save()

