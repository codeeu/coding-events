import datetime
import json
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse


from models.events import Event


class EventViewsTestCase(TestCase):
	def setUp(self):
		pending = Event.objects.create(
			organizer="Organizer 1",
			title="Event 1 - Pending",
			description="Some description - Pending",
			location="Near here",
			start_date=datetime.datetime.now(),
			end_date=datetime.datetime.now(),
			event_url="http://eee.com",
			contact_person="ss@ss.com",
			country="SI",
			pub_date=datetime.datetime.now(),
			tags=["tag1", "tag2"])

		client = Client()

	def test_index_view_without_approved_events(self):
		response = self.client.get(reverse('web.index'), {}, REMOTE_ADDR='93.103.53.11')

		self.assertEquals(200, response.status_code)
		self.assertJSONEqual('[]', response.context['map_events'])
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
			title="Event 1 - Approved",
			description="Some description - Approved",
			location="Near here",
			start_date=datetime.datetime.now(),
			end_date=datetime.datetime.now(),
			event_url="http://eee.com",
			contact_person="ss@ss.com",
			country="SI",
			pub_date=datetime.datetime.now(),
			tags=["tag1", "tag2"])

		response = self.client.get(reverse('web.index'), {}, REMOTE_ADDR='93.103.53.11')

		expected_map_events_result = json.dumps([
			{'fields': {'geoposition': '0,0', 'slug': 'event-1-approved', 'title': 'Event 1 - Approved'},
			 'model': 'api.event',
			 'pk': 2}
		])

		#assert
		self.assertJSONEqual(expected_map_events_result, response.context['map_events'])
		self.assertEquals('SI', response.context['country']['country_code'])
		self.assertEquals(1, len(response.context['latest_events']))
		self.assertEquals(aproved.title, response.context['latest_events'][0].title)


