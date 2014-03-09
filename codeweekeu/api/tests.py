import datetime
from django.test import TestCase
from api.models import Event
from api.processors import get_all_events
from api.processors import get_approved_events
from api.processors import get_pending_events
from api.processors import get_event_by_id


class EventTestCase(TestCase):
	def setUp(self):
		Event.objects.create(
			organizer='asdasd',
			title='asdasd',
			description='asdsad',
			location='asdsad',
			start_date=datetime.datetime.now(),
			end_date=datetime.datetime.now(),
			event_url='http://eee.com',
			contact_person='ss@ss.com',
			country='SI',
			pub_date=datetime.datetime.now())


	def test_get_all_events_with_one_event(self):
		all_events = get_all_events()
		self.assertEqual(1, all_events.count())


	def test_get_all_events_with_two_events(self):
		Event.objects.create(
			organizer='asdasd1',
			title='asdasd1',
			description='asdsad1',
			location='asdsad1',
			start_date=datetime.datetime.now(),
			end_date=datetime.datetime.now(),
			event_url='http://eee.com',
			contact_person='ss@ss.com',
			country='SI',
			pub_date=datetime.datetime.now())

		all_events = get_all_events()
		self.assertEqual(2, all_events.count())

	def test_get_all_events_with_different_statuses(self):
		new_event = Event.objects.create(
			organizer='asdasd1',
			title='asdasd1',
			description='asdsad1',
			location='asdsad1',
			start_date=datetime.datetime.now(),
			end_date=datetime.datetime.now(),
			event_url='http://eee.com',
			contact_person='ss@ss.com',
			country='SI',
			pub_date=datetime.datetime.now())
		new_event.status = 'APPROVED'
		new_event.save()

		self.assertEqual('PENDING', get_event_by_id(1).status)
		self.assertEqual('APPROVED', new_event.status)
		
		all_events = get_all_events()
		self.assertEqual(2, all_events.count())

	def test_get_approved_events(self):
		test_event = Event.objects.get(title='asdasd')
		self.assertEqual('PENDING', test_event.status)
		test_event.status = 'APPROVED'
		test_event.save()
		self.assertEqual('APPROVED', test_event.status)


	def test_get_approved_events_limited_to_one_ordered_by_title_desc(self):
		new_event = Event.objects.create(
			organizer='asdasd1',
			title='asdasd1',
			description='asdsad1',
			location='asdsad1',
			start_date=datetime.datetime.now(),
			end_date=datetime.datetime.now(),
			event_url='http://eee.com',
			contact_person='ss@ss.com',
			country='SI',
			pub_date=datetime.datetime.now())
		new_event.status = 'APPROVED'
		new_event.save()
		approved = get_approved_events(limit=1,order='-title')
		self.assertEquals(1, approved.count())
		self.assertEquals('asdasd1', approved[0].title)


	def test_get_pending_events(self):
		pending = get_pending_events()
		self.assertEqual(1, pending.count())


	def test_get_pending_events_when_there_is_none(self):
		test_event = Event.objects.get(title='asdasd')
		test_event.status = 'APPROVED'
		test_event.save()
		self.assertFalse(get_pending_events().exists())


	def test_get_pending_events_for_country(self):
		pending = get_pending_events(country_code='SI')
		self.assertEqual(1, pending.count())


	def test_get_pending_events_limit_to_one_ordered_by_location_desc(self):
		Event.objects.create(organizer='asdasd1',
			title='asdasd1',
			description='asdsad1',
			location='asdsad1',
			start_date=datetime.datetime.now(),
			end_date=datetime.datetime.now(),
			event_url='http://eee.com',
			contact_person='ss@ss.com',
			country='SI',
			pub_date=datetime.datetime.now())

		pending = get_pending_events(limit=1, order='-location')
		self.assertEquals(1, pending.count())
		self.assertEquals('asdasd1', pending[0].title)


	def test_get_event_by_id_without_id(self):
		with self.assertRaises(TypeError):
			test_event = get_event_by_id()


	def test_get_event_by_id_ok(self):
		test_event = get_event_by_id(1)
		self.assertEqual(1, test_event.pk)