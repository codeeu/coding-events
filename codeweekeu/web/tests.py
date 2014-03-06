import datetime
from django.test import TestCase
from django.db import IntegrityError
from django_countries import countries
from models.events import Event
from geoposition import Geoposition
from processors.event import get_event, create_or_update_event

class EventTestCase(TestCase):
	def setUp(self):
		Event.objects.create(organizer="asdasd",title="asdasd",
							description="asdsad",location="asdsad",
							start_date=datetime.datetime.now(),end_date=datetime.datetime.now(),
							event_url="http://eee.com",contact_person="ss@ss.com",country="SI",
							pub_date=datetime.datetime.now(),
							tags=["tag1","tag2"])

	def test_get_event(self):
		test_event = Event.objects.get(title="asdasd")
		self.assertEqual(test_event, get_event(event_id=1))

	def test_create_or_update_event(self):
		test_event = create_or_update_event(event_id=1)
		self.assertEqual(1, test_event.id)

	def test_create_event_without_args(self):
		with self.assertRaises(IntegrityError):
			test_event = create_or_update_event()

	def test_create_event_with_title_only(self):
		with self.assertRaises(IntegrityError):
			test_event = create_or_update_event(title="event title")

	def test_create_event_with_organizer_only(self):
		with self.assertRaises(IntegrityError):
			event_data = {"organizer":"asdasd"}
			test_event = create_or_update_event(**event_data)


	def test_create_event_with_start_end_dates_only(self):
		with self.assertRaises(IntegrityError):
			test_event = create_or_update_event(start_date=datetime.datetime.now(), end_date=datetime.datetime.now())


	def test_create_event_from_dictionary_with_missing_required_fields(self):
		with self.assertRaises(IntegrityError):
			event_data = {
				"end_date":datetime.datetime.now(),
				"start_date":datetime.datetime.now(),
				"organizer": "some organizer"
				}
			test_event = create_or_update_event(**event_data)

	def test_create_event_from_dictionary_with_all_required_fields(self):
		event_data = {
				"end_date":datetime.datetime.now(),
				"start_date":datetime.datetime.now(),
				"organizer": "some organizer",
				"title": "event title",
				"pub_date":datetime.datetime.now(),
				}
		test_event = create_or_update_event(**event_data)
		self.assertEqual(2, test_event.pk)
		self.assertEqual("event title", test_event.title)


	def test_create_event_from_dict_with_all_fields(self):
		event_data = {
		"end_date":datetime.datetime.now(),
		"start_date":datetime.datetime.now(),
		"organizer": "some organizer",
		"title": "event title",
		"pub_date":datetime.datetime.now(),
		"country": "SI",
		"geoposition": Geoposition(46.05528,14.51444),
		"location": "Ljubljana",
		"tags": ["tag1", "tag2"]
		}
		test_event = create_or_update_event(**event_data)
		self.assertEqual(2, test_event.pk)
		self.assertEqual("Ljubljana", test_event.location)
		self.assertEqual("46.05528", str(test_event.geoposition.latitude))
		self.assertIn("tag1",test_event.tags.names())
		self.assertIn("tag2",test_event.tags.names())

