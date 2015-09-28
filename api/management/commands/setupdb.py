import sys
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = 'Creates django database, creates superusers.'

    def handle(self, *args, **options):
        # Admin superuser username and password
        ADMIN_USERNAME = 'admin'
        ADMIN_PASSWORD = '12345!'

        # Db properties
        db_engine = settings.DATABASES['default']['ENGINE'].split('.')[-1]
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_pass = settings.DATABASES['default']['PASSWORD']

        sys.stdout.write('Database engine detected: %s\n\n' % db_engine)

        # If engine is sqlite, remove db file
        if db_engine == 'sqlite3':
            sys.stdout.write('Removing %s ... \n' % db_name)
            db_filepath = os.path.join(settings.DJANGO_ROOT, 'db', db_name)
            if os.path.exists(db_filepath):
                os.unlink(db_filepath)
        else:
            sys.stdout.write('Database engines supported: sqlite3.\n')
            return

        # Run syncdb
        call_command('syncdb', interactive=False)

        # Create admin superuser
        User.objects.create_superuser(
            ADMIN_USERNAME, 'admin@email.com', ADMIN_PASSWORD)

        call_command('migrate')
