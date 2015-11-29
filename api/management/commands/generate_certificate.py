# coding=utf8
from django.core.management.base import BaseCommand, CommandError
from certificates.generator import *
from api.models import Event

class Command(BaseCommand):
    args = '<event-id> [<event-id>, ...]'
    help = """
    Generates or regenerates a certificate for a given event.
    """

    def handle(self, *args, **options):
        if not args:
            self.stderr.write('Please provide at least one event ID.')

        for event_id in args:
            self.stdout.write('Regenerating the certificate for event ID %s...' % event_id)

            try:
                event = Event.objects.get(pk=int(event_id))
            except Event.DoesNotExist:
                self.stderr.write('Event ID "%s" does not exist.' % event_id)
                continue

            path = generate_certificate_for(event.pk, event.certificate_file_name(), event.name_for_certificate)

            if path:
                self.stdout.write('Certificate for event ID %s geenrated successfully: %s' % (event_id, path))
            else:
                self.stderr.write('An error occurred while generating the certificate.')
