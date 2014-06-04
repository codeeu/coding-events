import datetime
import json
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from models.events import Event
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
		self.assertJSONEqual('[]', json.loads(response.context['map_events']))
		self.assertEquals((46.0, 15.0), response.context['lan_lon'])
		self.assertQuerysetEqual([], response.context['latest_events'])
		self.assertTemplateUsed(response, 'pages/index.html')

	def test_index_view_changing_remote_in_request(self):
		#setup
		response = self.client.get(reverse('web.index'), {},
		                           HTTP_X_FORWARDED_FOR='93.103.53.11, 93.103.53.11')

		#assert
		self.assertEquals(200, response.status_code)
		self.assertEquals((46.0, 15.0), response.context['lan_lon'])

	def test_index_with_approved_events(self):
		#setup
		aproved = Event.objects.create(
			status="APPROVED",
			organizer="Organizer 1",
			creator=User.objects.filter(pk=1)[0],
			title="Event 1 - Approved",
			description="Some description - Approved",
			location="Near here",
			start_date=datetime.datetime.now() + datetime.timedelta(days=1, hours=3),
			end_date=datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
			event_url="http://eee.com",
			contact_person="ss@ss.com",
			country="SI",
			pub_date=datetime.datetime.now(),
			tags=["tag1", "tag2"])

		response = self.client.get(reverse('web.index'), {}, REMOTE_ADDR='93.103.53.11')

		expected_map_events_result = json.dumps([
			{'pk': 2, 'model': 'api.event', 'fields': 
			{'picture': '', 'slug': 'event-1-approved', 'title': 'Event 1 - Approved', 
			'description': 'Some description - Approved', 'geoposition': '0,0', },	 
			 }
		])

		#assert
		self.assertJSONEqual(expected_map_events_result, json.loads(response.context['map_events']))
		self.assertEquals('SI', response.context['country']['country_code'])
		self.assertEquals(1, len(response.context['latest_events']))
		self.assertEquals(aproved.title, response.context['latest_events'][0].title)

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

