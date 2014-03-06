import datetime
from django.test import TestCase
from api.models import Event
from api.processors import get_pending_events


class EventTestCase(TestCase):
	def setUp(self):
		Event.objects.create(
			organizer="asdasd",
			title="asdasd",
			description="asdsad",
			location="asdsad",
			start_date=datetime.datetime.now(),
			end_date=datetime.datetime.now(),
			event_url="http://eee.com",
			contact_person="ss@ss.com",
			country="SI",
			pub_date=datetime.datetime.now())

	def test_get_approved_events(self):
		test_event = Event.objects.get(title="asdasd")
		self.assertEqual("PENDING", test_event.status)
		test_event.status = "APPROVED"
		test_event.save()
		self.assertEqual("APPROVED", test_event.status)

	def test_get_pending_events(self):
		events = get_pending_events()
		self.assertEqual(1, len(events))
