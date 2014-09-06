# -*- coding: utf-8 -*-
import json
import datetime

from geoposition import Geoposition

from web.processors.event import create_or_update_event


class TestRestApi:
	def test_event_list_all(self, client, admin_user):
		event_data = {
			"start_date": datetime.datetime.now() - datetime.timedelta(days=1, hours=3),
			"end_date": datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
			"organizer": "some organizer",
			"creator": admin_user,
			"title": "Unique REST API Event",
			"pub_date": datetime.datetime.now(),
			"country": "SI",
			"geoposition": Geoposition(46.05528,14.51444),
			"location": "Ljubljana",
			"audience": [1],
			"theme": [1],
			"tags": ["tag1", "tag2"],
		}

		event = create_or_update_event(**event_data)
		event.status = 'APPROVED'
		event.save()

		response_json = client.get('/api/event/list/?format=json')
		response_data = json.loads(response_json.content)

		assert isinstance(response_data, list)
		assert event_data['title'] in response_json.content
