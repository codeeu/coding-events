import datetime
import StringIO
import pytest
from django.test import TestCase
from django.db import IntegrityError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
from py.path import local

from geoposition import Geoposition

from api.models.events import Event
from api.models import UserProfile
from api.processors import get_event_by_id
from web.processors.event import create_or_update_event
from web.processors.event import change_event_status
from web.processors.event import reject_event_status
from api.processors import get_approved_events
from api.processors import get_next_or_previous
from api.processors import get_nearby_events


class EventTestCase(TestCase):
	def get_user(self):
		return User.objects.get(pk=1)

	def create_event(self, title="Event title",
		start_date=datetime.datetime.now() + datetime.timedelta(days=0, hours=3), 
		end_date=datetime.datetime.now() + datetime.timedelta(days=1, hours=3),
		country_code="SI", status="PENDING"):

		event_data = {
			"end_date": start_date,
			"start_date": end_date,
			"organizer": "Test organizer",
			"creator": self.get_user(),
			"title": title,
			"pub_date": datetime.datetime.now(),
			"country": country_code,
			"geoposition": "46.05528,14.51444",
			"location": "Ljubljana",
			"audience": [1],
			"theme": [1],
			"status": status,
		}
		return create_or_update_event(**event_data)

	def setUp(self):
		self.u1 = User.objects.create(username='user1')
		self.up1 = UserProfile.objects.create(user=self.u1)

		Event.objects.create(organizer="asdasd",
			creator=User.objects.filter(pk=1)[0],
			title="asdasd",
			description="asdsad",
			location="asdsad",
			start_date=datetime.datetime.now(),
			end_date=datetime.datetime.now(),
			event_url="http://eee.com",
			contact_person="ss@ss.com",
			country="SI",
			audience=[1],
			theme=[1],
			pub_date=datetime.datetime.now(),
			tags=["tag1", "tag2"])

	def test_get_event(self):
		test_event = Event.objects.get(title="asdasd")
		self.assertEqual(test_event, get_event_by_id(event_id=1))

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
				"end_date": datetime.datetime.now(),
				"start_date": datetime.datetime.now(),
				"organizer": "some organizer"
			}
			test_event = create_or_update_event(**event_data)

	def test_create_event_from_dictionary_with_all_required_fields(self):
		event_data = {
				"end_date": datetime.datetime.now(),
				"start_date": datetime.datetime.now(),
				"organizer": "some organizer",
				"creator": User.objects.filter(pk=1)[0],
				"title": "event title",
				"pub_date": datetime.datetime.now(),
		}
		test_event = create_or_update_event(**event_data)
		self.assertEqual(2, test_event.pk)
		self.assertEqual("event title", test_event.title)

	def test_create_event_from_dict_with_all_fields(self):
		with open(local(__file__).dirname + '/../../static/img/team/alja.jpg') as fp:
			io = StringIO.StringIO()
			io.write(fp.read())
			uploaded_picture = InMemoryUploadedFile(io, None, "alja.jpg", "jpeg", io.len, None)
			uploaded_picture.seek(0)

		event_data = {
			"end_date": datetime.datetime.now(),
			"start_date": datetime.datetime.now(),
			"organizer": "some organizer",
			"creator": User.objects.filter(pk=1)[0],
			"title": "event title",
			"pub_date": datetime.datetime.now(),
			"country": "SI",
			"geoposition": Geoposition(46.05528,14.51444),
			"location": "Ljubljana",
			"audience": [1],
			"theme": [1],
			"tags": ["tag1", "tag2"],
			"picture": uploaded_picture
		}

		test_event = create_or_update_event(**event_data)
		self.assertEqual(2, test_event.pk)
		self.assertEqual("Ljubljana", test_event.location)
		self.assertEqual("46.05528", str(test_event.geoposition.latitude))
		self.assertIn("tag1", test_event.tags.names())
		self.assertIn("tag2", test_event.tags.names())

		assert 'event_picture/alja' in test_event.picture.path

	def test_get_approved_event_without_filter_returns_zero(self):

		events = get_approved_events()
		self.assertQuerysetEqual([], events)

	def test_get_approved_event_without_filter_with_pending_event(self):
		self.create_event(start_date=datetime.datetime.now() + datetime.timedelta(days=0, hours=3),
			end_date=datetime.datetime.now() + datetime.timedelta(days=1, hours=3),
			status="APPROVED",)
		events = get_approved_events()
		self.assertEqual(1, len(events))

	def test_get_approved_event_without_filter_with_approved_event_but_passed_date(self):
		self.create_event(start_date=datetime.datetime.now() - datetime.timedelta(days=1, hours=3),
			end_date=datetime.datetime.now() - datetime.timedelta(days=2, hours=3),
			status="APPROVED")
		events = get_approved_events()
		self.assertEqual(0, len(events))

	def test_get_approved_event_with_filter_country_code_with_approved_event(self):
		self.create_event(country_code="IS", status="APPROVED")
		events = get_approved_events(country_code="IS")
		self.assertEqual(1, len(events))
		self.assertEqual("IS", events[0].country.code)

	def test_get_approved_event_with_filter_country_code_and_order_with_approved_event(self):
		countries = ["IS", "DK", "FI", "FI", "LI"]
		for index, country in enumerate(countries):
			self.create_event(title="Testing event" + str(index + 1), country_code=country, status="APPROVED",
				start_date=datetime.datetime.now() + datetime.timedelta(days=0, hours=index + 1),
				end_date=datetime.datetime.now() + datetime.timedelta(days=1, hours=index + 1))

		events = get_approved_events(order="start_date")
		self.assertEqual(5, len(events))
		self.assertEqual("IS", events[0].country.code)
		self.assertEqual("DK", events[1].country.code)
		self.assertEqual("FI", events[2].country.code)
		self.assertEqual("FI", events[3].country.code)
		self.assertEqual("LI", events[4].country.code)

	def test_get_approved_event_with_filter_country_code_and_order_and_limit__with_approved_event(self):
		countries = ["IS", "DK", "FI", "FI", "FI"]
		for index, country in enumerate(countries):
			self.create_event(title="Testing event" + str(index + 1), country_code=country, status="APPROVED",
				start_date=datetime.datetime.now() + datetime.timedelta(days=0, hours=index + 1),
				end_date=datetime.datetime.now() + datetime.timedelta(days=1, hours=index + 1))

		events = get_approved_events(order="start_date", limit=2, country_code="FI")
		self.assertEqual(2, len(events))
		self.assertEqual("Testing event3", events[0].title)
		self.assertEqual("Testing event4", events[1].title)

	def test_get_next_or_previous_pending_event(self):
		statuses = ["PENDING", "APPROVED", "PENDING"]

		for status in statuses:
			event = self.create_event(status=status)
			
		test_event = Event.objects.get(pk=2)
		next_event = get_next_or_previous(test_event)

		self.assertEqual(4, next_event.pk)

		test_event_2 = Event.objects.get(pk=4)
		next_event_2 = get_next_or_previous(test_event_2)

		self.assertEqual(None, next_event_2)

		test_event_3 = Event.objects.get(pk=4)
		previous_event = get_next_or_previous(test_event_3, direction=False)

		self.assertEqual(2, previous_event.pk)

		test_event_4 = Event.objects.get(pk=1)
		previous_event_2 = get_next_or_previous(test_event_4, direction=False)

		self.assertEqual(None, previous_event_2)

	def test_get_nearby_events(self):
		target_event = self.create_event(status="APPROVED")
		nearby_event = self.create_event(status="APPROVED")
		nearby = get_nearby_events(target_event)

		self.assertEqual(1, len(nearby))
		self.assertEqual(nearby_event.pk, nearby[0].pk)

		self.create_event(status="APPROVED", country_code="HR")
		nearby = get_nearby_events(target_event)
		
		self.assertEqual(1, len(nearby))

		self.create_event(status="PENDING")
		nearby = get_nearby_events(target_event)

		self.assertEqual(1, len(nearby))

	def test_change_event_status(self):
		pending_event = self.create_event(status="PENDING")
		approved = change_event_status(pending_event.id)

		self.assertEqual(approved.status, "APPROVED")

		test_event = Event.objects.get(pk=pending_event.id)
		self.assertEqual(test_event.status, "APPROVED")

		approved_event = self.create_event(status="APPROVED")
		pending = change_event_status(approved_event.id)

		test_event1 = Event.objects.get(pk=approved_event.id)
		self.assertEqual(test_event1.status, "PENDING")


	def test_reject_event_status(self):
		pending_event = self.create_event(status="PENDING")
		reject = reject_event_status(pending_event.id)

		test_event = Event.objects.get(pk=pending_event.id)
		self.assertEqual(test_event.status, "REJECTED")

		rejected_event = self.create_event(status="REJECTED")
		pending = reject_event_status(rejected_event.id)

		test_event1 = Event.objects.get(pk=rejected_event.id)
		self.assertEqual(test_event1.status, "PENDING")

	def test_edit_event_with_all_fields(self):
		# First create a new event
		with open(local(__file__).dirname + '/../../static/img/team/alja.jpg') as fp:
			io = StringIO.StringIO()
			io.write(fp.read())
			uploaded_picture = InMemoryUploadedFile(io, None, "alja.jpg", "jpeg", io.len, None)
			uploaded_picture.seek(0)

		event_data = {
			"end_date": datetime.datetime.now(),
			"start_date": datetime.datetime.now(),
			"organizer": "some organizer",
			"creator": User.objects.filter(pk=1)[0],
			"title": "event title",
			"pub_date": datetime.datetime.now(),
			"country": "SI",
			"geoposition": Geoposition(46.05528,14.51444),
			"location": "Ljubljana",
			"audience": [1],
			"theme": [1],
			"tags": ["tag1", "tag2"],
			"picture": uploaded_picture
		}

		test_event = create_or_update_event(**event_data)

		# Then edit it
		with open(local(__file__).dirname + '/../../static/img/team/ercchy.jpg') as fp:
			io = StringIO.StringIO()
			io.write(fp.read())
			uploaded_picture = InMemoryUploadedFile(io, None, "ercchy.jpg", "jpeg", io.len, None)
			uploaded_picture.seek(0)

		event_data = {
			"end_date": datetime.datetime.now(),
			"start_date": datetime.datetime.now(),
			"organizer": "another organiser",
			"creator": User.objects.filter(pk=1)[0],
			"title": "event title - edited",
			"pub_date": datetime.datetime.now(),
			"country": "SI",
			# "geoposition": Geoposition(46.05528,14.51444),
			"location": "Ljubljana",
			"audience": [1],
			"theme": [1],
			"tags": ["tag3", "tag4"],
			"picture": uploaded_picture
		}
		test_event = create_or_update_event(event_id=test_event.id, **event_data)
		assert "tag1" not in test_event.tags.names()

		assert 'event_picture/alja' not in test_event.picture
		assert 'event_picture/ercchy' in test_event.picture.path

@pytest.mark.django_db
def test_create_event_in_moldova(admin_user, db):

	event_data = {
		'audience': [3],
		'theme': [1,2],
		'contact_person': u'test@example.com',
		'country': u'MD',
		'description': u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\r\ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\r\nquis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\r\nconsequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\r\ncillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\r\nproident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
		'event_url': u'',
		'location': u'Tiraspol, Moldova',
		'organizer': u'RailsGirls Moldova',
		"creator": admin_user,
		'start_date': datetime.datetime.now(),
		'end_date': datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
		'tags': [u'css', u'html', u'web'],
		'title': u'Rails Moldova',
	}

	test_event = create_or_update_event(event_id=None, **event_data)

	assert "MD" == test_event.country.code

@pytest.mark.django_db
def test_create_event_in_kosovo(admin_user, db):
	event_data = {
		'audience': [3],
		'theme': [1,2],
		'contact_person': u'test@example.com',
		'country': u'XK',
		'description': u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\r\ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\r\nquis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\r\nconsequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\r\ncillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\r\nproident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
		'event_url': u'',
		'location': u'Shaban Polluzha, Prishtina, Kosova (Kosovo)',
		'organizer': u'RailsGirls Kosovo',
		"creator": admin_user,
		'start_date': datetime.datetime.now(),
		'end_date': datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
		'tags': [u'css', u'html', u'web'],
		'title': u'RailsGirls Kosovo',
	}

	test_event = create_or_update_event(event_id=None, **event_data)

	assert "XK" == test_event.country.code

