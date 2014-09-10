import datetime
import json
import pytest
import StringIO
import os

from py.path import local
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile

from api.models.events import Event
from django.contrib.auth.models import User
from api.models import UserProfile


class EventViewsTestCase(TestCase):
	def setUp(self):
		self.u1 = User.objects.create(username='user1')
		self.up1 = UserProfile.objects.create(user=self.u1)

		pending = Event.objects.create(
			organizer="Organizer 1",
			creator=User.objects.filter(pk=1)[0],
			title="Event 1 - Pending",
			description="Some description - Pending",
			location="Near here",
			start_date=datetime.datetime.now() + datetime.timedelta(days=1, hours=3),
			end_date=datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
			event_url="http://eee.com",
			contact_person="ss@ss.com",
			country="SI",
			pub_date=datetime.datetime.now(),
			tags=["tag1", "tag2"])

		client = Client()

	def test_index_view_without_approved_events(self):
		response = self.client.get(reverse('web.index'), {}, REMOTE_ADDR='93.103.53.11')

		self.assertEquals(200, response.status_code)
		self.assertEquals((46.0, 15.0), response.context['lan_lon'])
		self.assertEquals('SI', response.context['country']['country_code'])
		self.assertTemplateUsed(response, 'pages/index.html')

	def test_index_view_changing_remote_in_request(self):
		#setup
		response = self.client.get(reverse('web.index'), {},
		                           HTTP_X_FORWARDED_FOR='93.103.53.11, 93.103.53.11')

		#assert
		self.assertEquals(200, response.status_code)
		self.assertEquals((46.0, 15.0), response.context['lan_lon'])

	def test_view_event_without_picture(self):
		#setup
		test_event = Event.objects.create(
			organizer="Organizer 1",
			creator=User.objects.filter(pk=1)[0],
			title="Test View Event Without Picture",
			description="Some description",
			location="Near here",
			start_date=datetime.datetime.now() + datetime.timedelta(days=1, hours=3),
			end_date=datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
			event_url="http://eee.com",
			contact_person="ss@ss.com",
			country="SI",
			pub_date=datetime.datetime.now(),
			tags=["tag1", "tag2"])

		response = self.client.get(reverse('web.view_event', args=[test_event.pk, test_event.slug]))

		#assert
		self.assertEquals(200, response.status_code)



	def test_search_events_with_search_query(self):
		#setup
		approved = Event.objects.create(
			status="APPROVED",
			organizer="Organizer 1",
			creator=User.objects.filter(pk=1)[0],
			title="Event Arglebargle - Approved",
			description="Some description - Approved",
			location="Near here",
			start_date=datetime.datetime.now() + datetime.timedelta(days=1, hours=3),
			end_date=datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
			event_url="http://eee.com",
			contact_person="ss@ss.com",
			country="SI",
			pub_date=datetime.datetime.now(),
			tags=["tag1", "tag2"])

		response = self.client.get(reverse('web.search_events'), {'q':'arglebargle'}, REMOTE_ADDR='93.103.53.11')

		#assert
		self.assertEquals(1,response.context['events'].count())
		self.assertEquals('SI', response.context['country'])

	def test_search_events_with_search_query_multiple_events(self):
		#setup
		approved1 = Event.objects.create(
			status="APPROVED",
			organizer="Organizer 1",
			creator=User.objects.filter(pk=1)[0],
			title="Event Arglebargle - Approved",
			description="Some description - Approved",
			location="Near here",
			start_date=datetime.datetime.now() + datetime.timedelta(days=1, hours=3),
			end_date=datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
			event_url="http://eee.com",
			contact_person="ss@ss.com",
			country="SI",
			pub_date=datetime.datetime.now(),
			tags=["tag1", "tag2"])
		approved2 = Event.objects.create(
			status="APPROVED",
			organizer="Organizer 2",
			creator=User.objects.filter(pk=1)[0],
			title="Event Arglebargle - Approved",
			description="Some description - Approved",
			location="Near here",
			start_date=datetime.datetime.now() + datetime.timedelta(days=1, hours=3),
			end_date=datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
			event_url="http://eee.com",
			contact_person="ss@ss.com",
			country="AT",
			pub_date=datetime.datetime.now(),
			tags=["tag1", "tag2"])

		response = self.client.get(reverse('web.search_events'), {'q':'arglebargle'}, REMOTE_ADDR='93.103.53.11')

		#assert
		self.assertEquals(1,response.context['events'].count())
		self.assertEquals('SI', response.context['country'])

	def test_search_events_with_search_query_all_countries_multiple_results(self):
		#setup
		approved1 = Event.objects.create(
			status="APPROVED",
			organizer="Organizer 1",
			creator=User.objects.filter(pk=1)[0],
			title="Event Arglebargle - Approved",
			description="Some description - Approved",
			location="Near here",
			start_date=datetime.datetime.now() + datetime.timedelta(days=1, hours=3),
			end_date=datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
			event_url="http://eee.com",
			contact_person="ss@ss.com",
			country="SI",
			pub_date=datetime.datetime.now(),
			tags=["tag1", "tag2"])
		approved2 = Event.objects.create(
			status="APPROVED",
			organizer="Organizer 2",
			creator=User.objects.filter(pk=1)[0],
			title="Event Arglebargle - Approved",
			description="Some description - Approved",
			location="Near here",
			start_date=datetime.datetime.now() + datetime.timedelta(days=1, hours=3),
			end_date=datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
			event_url="http://eee.com",
			contact_person="ss@ss.com",
			country="AT",
			pub_date=datetime.datetime.now(),
			tags=["tag1", "tag2"])

		response = self.client.get(reverse('web.search_events'), {'q':'arglebargle', 'country_code':'00'}, REMOTE_ADDR='93.103.53.11')

		#assert
		self.assertEquals(2,response.context['events'].count())

@pytest.mark.django_db
def test_create_event_with_image(admin_user, admin_client, db):
	with open(local(__file__).dirname + '/../../static/img/team/alja.jpg') as fp:
		io = StringIO.StringIO()
		io.write(fp.read())
		uploaded_picture = InMemoryUploadedFile(io, None, "alja.jpg", "jpeg", io.len, None)
		uploaded_picture.seek(0)

	event_data = {
		'audience': [4, 5],
		'theme': [1,2],
		'contact_person': u'test@example.com',
		'country': u'SI',
		'description': u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\r\ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\r\nquis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\r\nconsequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\r\ncillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\r\nproident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
		'event_url': u'',
		'location': u'Ljubljana, Slovenia',
		'organizer': u'Mozilla Slovenija',
		'picture': uploaded_picture,
		'start_date': datetime.datetime.now(),
		'end_date': datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
		'tags': [u'css', u'html', u'web'],
		'title': u'Webmaker Ljubljana',
		'user_email': u'test@example.com'
	}

	response = admin_client.post(reverse('web.add_event'), event_data)

	assert response.status_code == 302

	response = admin_client.get(response.url)
	assert 'event_picture/alja' in response.content

@pytest.mark.django_db
def test_edit_event_with_image(admin_user, admin_client, db):
	# First create event
	with open(local(__file__).dirname + '/../../static/img/team/alja.jpg') as fp:
		io = StringIO.StringIO()
		io.write(fp.read())
		uploaded_picture = InMemoryUploadedFile(io, None, "alja17.jpg", "jpeg", io.len, None)
		uploaded_picture.seek(0)

	event_data = {
		'audience': [4, 5],
		'theme': [1,2],
		'contact_person': u'test@example.com',
		'country': u'SI',
		'description': u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\r\ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\r\nquis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\r\nconsequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\r\ncillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\r\nproident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
		'event_url': u'',
		'location': u'Ljubljana, Slovenia',
		'organizer': u'Mozilla Slovenija',
		'picture': uploaded_picture,
		'start_date': datetime.datetime.now(),
		'end_date': datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
		'tags': [u'css', u'html', u'web'],
		'title': u'Webmaker Ljubljana',
		'user_email': u'test@example.com'
	}

	response = admin_client.post(reverse('web.add_event'), event_data)

	assert response.status_code == 302

	response = admin_client.get(response.url)
	assert 'event_picture/alja' in response.content

	event = Event.objects.latest('id')

	# Then edit it
	with open(local(__file__).dirname + '/../../static/img/team/ercchy.jpg') as fp:
		io = StringIO.StringIO()
		io.write(fp.read())
		uploaded_picture = InMemoryUploadedFile(io, None, "ercchy.jpg", "jpeg", io.len, None)
		uploaded_picture.seek(0)

	event_data = {
		'audience': [6, 7],
		'theme': [3,4],
		'contact_person': u'another_person@example.com',
		'country': u'SI',
		'description': u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\r\ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\r\nquis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\r\nconsequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\r\ncillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\r\nproident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
		'event_url': u'',
		'location': u'Ljubljana, Slovenia',
		'organizer': u'Mozilla Slovenija',
		'picture': uploaded_picture,
		'start_date': datetime.datetime.now(),
		'end_date': datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
		'tags': [u'css', u'html', u'web'],
		'title': u'Webmaker Ljubljana',
		'user_email': u'another_person@example.com'
	}

	response_edited = admin_client.post(reverse('web.edit_event', args=[event.id]), event_data)
	assert response_edited.status_code == 302

	response = admin_client.get(event.get_absolute_url())
	assert 'event_picture/alja17' not in response.content
	assert 'event_picture/ercchy' in response.content

	#Check if the old event picture has been deleted
	old_picture = os.path.isfile(local(__file__).dirname+'/../../media/event_picture/alja17.jpg')

	assert not old_picture

	event_data = {
		'audience': [6, 7],
		'theme': [3,4],
		'contact_person': u'another_person@example.com',
		'country': u'SI',
		'description': u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\r\ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\r\nquis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\r\nconsequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\r\ncillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\r\nproident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
		'event_url': u'',
		'location': u'Ljubljana, Slovenia',
		'organizer': u'Mozilla Slovenija',
		'picture': '',
		'start_date': datetime.datetime.now(),
		'end_date': datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
		'tags': [u'css', u'html', u'web'],
		'title': u'Webmaker Ljubljana',
		'user_email': u'another_person@example.com'
	}

	response_edited = admin_client.post(reverse('web.edit_event', args=[event.id]), event_data)
	assert response_edited.status_code == 302

	response = admin_client.get(event.get_absolute_url())
	assert 'event_picture/ercchy' not in response.content







