import datetime
from django.test import TestCase
from mailer.event_report_mailer import send_event_report_email

from api.models.events import Event
from django.contrib.auth.models import User
from api.models import UserProfile

from django.core import mail


class EmailTestCase(TestCase):

    def setUp(self):
        self.u1 = User.objects.create(
            username='user1',
            email='info@example.com',
            first_name='Nejc')
        self.up1 = UserProfile.objects.create(user=self.u1)

        self.event = Event.objects.create(
            organizer="Organizer 1",
            creator=User.objects.filter(
                pk=1)[0],
            title="Event 1 - Pending",
            description="Some description - Pending",
            location="Near here",
            start_date=datetime.datetime.now() +
            datetime.timedelta(
                days=1,
                hours=3),
            end_date=datetime.datetime.now() +
            datetime.timedelta(
                days=3,
                hours=3),
            event_url="http://eee.com",
            contact_person="ss@ss.com",
            country="SI",
            pub_date=datetime.datetime.now(),
            tags=[
                    "tag1",
                "tag2"])

    def test_send_event_email(self):
        send_event_report_email(self.u1, self.event)
        email = mail.outbox[0]

        self.assertEquals(
            'A new event on codeweek.eu needs your attention',
            email.subject)
        self.assertEquals('info@codeweek.eu', email.from_email)
        self.assertEquals([self.u1.email], email.to)
        self.assertIn(self.u1.first_name, email.body)
        self.assertIn(self.event.title, email.body)
