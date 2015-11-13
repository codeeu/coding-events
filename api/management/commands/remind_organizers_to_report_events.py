from datetime import datetime, timedelta
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from api.processors import events_pending_for_report
from api.processors import events_pending_for_report_for
from api.models.users import User
from mailer.event_report_mailer import send_reminder_for_event_report_and_certificate

class Command(BaseCommand):
    args = '<emails-per-run>'
    help = """
    Sends a notification email to each organizer with unreported events.
    Only a limited number of emails is sent per run. Should be run via a cron.
    """

    option_list = BaseCommand.option_list + (
        make_option('--simulate-emails',
            action='store_true',
            dest='simulate_emails',
            default=False,
            help='Do not actually send emails, just print the contents to STDOUT.'
        ),
        make_option('--simulate-db',
            action='store_true',
            dest='simulate_db',
            default=False,
            help='Do not actually update the DB to mark events as notified.'
        ),
        make_option('--emails-per-run',
            type='int',
            action='store',
            dest='emails_per_run',
            help='Required. The number of emails to send per run.'
        ),
        make_option('--notifications-limit',
            type='int',
            action='store',
            dest='notifications_limit',
            default=3,
            help='Send at most X notification emails for event reporting.'
        ),
        make_option('--notifications-interval-in-days',
            type='int',
            action='store',
            dest='notifications_interval_in_days',
            default=21,
            help="If we're allowed to send more than one reminder email, notifications will be sent each X days."
        ),
    )

    def handle(self, *args, **options):
        last_reminder_sent_before = datetime.now() - timedelta(days=options['notifications_interval_in_days'])

        if options['emails_per_run'] == None:
            self.stderr.write(
                "Please specify the emails to send per run as a positional argument. E.g.:\n\n" +
                "manage.py remind_organizers_to_report_events --emails-per-run 100"
            )
            exit(1)

        events_to_report = events_pending_for_report().filter(
                Q(last_report_notification_sent_at=None) |
                Q(last_report_notification_sent_at__lte=last_reminder_sent_before)
            ).filter(
                report_notifications_count__lt=options['notifications_limit']
            ).order_by(
                'report_notifications_count', 'start_date'
            )

        organizer_ids = events_to_report.distinct().values_list('creator_id', flat=True)

        # The values above may not be unique as we're using ordering. See here for more info:
        # https://docs.djangoproject.com/en/1.6/ref/models/querysets/#django.db.models.query.QuerySet.distinct
        organizer_ids = list(set(organizer_ids))

        organizers = User.objects.filter(id__in=organizer_ids)

        self.stdout.write(
            u'We have to notify {organizers_count} organizer(s) in a total of {events_count} event(s). Will send at most {emails_per_run} email(s) now.'.format(
                events_count=events_to_report.count(),
                organizers_count=organizers.count(),
                emails_per_run=options['emails_per_run']
            )
        )

        for organizer in organizers[:options['emails_per_run']]:
            unreported_organizer_events = events_pending_for_report_for(organizer)
            unrepored_events_count = unreported_organizer_events.count()

            self.stdout.write(
                u'Emailing {contact} for {events_count} unreported event(s)'.format(
                    contact=organizer.email_with_name(),
                    events_count=unrepored_events_count
                )
            )

            send_reminder_for_event_report_and_certificate(
                organizer,
                unrepored_events_count,
                previous_emails_count=unreported_organizer_events[0].report_notifications_count,
                max_emails_count=options['notifications_limit'],
                test_mode=options['simulate_emails']
            )

            if not options['simulate_db']:
                for event in unreported_organizer_events:
                    event.last_report_notification_sent_at = datetime.now()
                    event.report_notifications_count += 1
                    event.save()
