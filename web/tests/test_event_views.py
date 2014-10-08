# coding=utf-8

import datetime
import pytest
import StringIO
import os

from py.path import local
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User

from api.models.events import Event
from api.models import UserProfile

from web.tests import EventFactory, ApprovedEventFactory

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
		test_event = EventFactory.create()
		response = self.client.get(reverse('web.view_event', args=[test_event.pk, test_event.slug]))

		assert response.status_code == 200
		assert test_event.title in response.content

		test_event.delete()


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

@pytest.mark.django_db
def test_nonexistent_event(db, client):
	response = client.get(reverse('web.view_event', args=[1234, 'shouldnt-exist']))

	assert response.status_code == 404

@pytest.mark.django_db
def test_geoip_slovenian_ip(db, client):
	response = client.get('/', REMOTE_ADDR='93.103.53.1')

	assert 'List all events in <span id="country"> Slovenia' in response.content

@pytest.mark.django_db
def test_geoip_invalid_ip(db, client):
	response = client.get('/', REMOTE_ADDR='127.0.0.1')

	assert 'List all events' in response.content
	assert 'List all events <span' not in response.content

@pytest.mark.django_db
def test_list_events_for_country_code(db, client):
	response = client.get(reverse('web.view_event_by_country', args=['SI']))

	assert response.status_code == 200
