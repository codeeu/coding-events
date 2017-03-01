# -*- coding: utf-8 -*-
import json
import datetime

from geoposition import Geoposition

from web.processors.event import create_or_update_event


class TestRestApi:

    def test_event_list_all(self, client, admin_user):
        event_data = {
            "start_date": datetime.datetime.now() -
            datetime.timedelta(
                days=1,
                hours=3),
            "end_date": datetime.datetime.now() +
            datetime.timedelta(
                days=3,
                hours=3),
            "organizer": "some organizer",
            "creator": admin_user,
            "title": "Unique REST API Event",
            "pub_date": datetime.datetime.now(),
            "country": "SI",
            "geoposition": "46.05528,14.51444",
            "location": "Ljubljana",
            "audience": [1],
            "theme": [1],
            "tags": [
                "tag1",
                "tag2"],
        }

        event = create_or_update_event(**event_data)
        event.status = 'APPROVED'
        event.save()

        response_json = client.get('/api/event/list/?format=json')
        response_data = json.loads(response_json.content)

        assert isinstance(response_data, list)
        assert event_data['geoposition'] in response_json.content

    def test_event_detail_all(self, client, admin_user):
        event_data = {
            "start_date": datetime.datetime.now() -
                          datetime.timedelta(
                              days=1,
                              hours=3),
            "end_date": datetime.datetime.now() +
                        datetime.timedelta(
                            days=3,
                            hours=3),
            "organizer": "some organizer",
            "creator": admin_user,
            "title": "Unique REST API Event",
            "pub_date": datetime.datetime.now(),
            "country": "SI",
            "geoposition": "46.05528,14.51444",
            "location": "Ljubljana",
            "audience": [1],
            "theme": [1],
            "tags": [
                "tag1",
                "tag2"],
        }

        event = create_or_update_event(**event_data)
        event.status = 'APPROVED'
        event.save()

        response_json = client.get('/api/event/detail/?id=1')
        response_data = json.loads(response_json.content)

        print response_data

        assert isinstance(response_data, list)
        assert response_data[0]["title"] == "Unique REST API Event"


    def test_scoreboard_api(self, client, admin_user):
        event_data = {
            "start_date": datetime.datetime.now() -
            datetime.timedelta(
                days=1,
                hours=3),
            "end_date": datetime.datetime.now() +
            datetime.timedelta(
                days=3,
                hours=3),
            "organizer": "some organizer",
            "creator": admin_user,
            "title": "Event in SI",
            "pub_date": datetime.datetime.now(),
            "country": "SI",
            "geoposition": Geoposition(
                46.05528,
                14.51444),
            "location": "Ljubljana",
            "audience": [1],
            "theme": [1],
            "tags": [
                "tag1",
                "tag2"],
        }

        event = create_or_update_event(**event_data)
        event.status = 'APPROVED'
        event.save()

        event_data = {
            "start_date": datetime.datetime.now() - datetime.timedelta(days=1, hours=3),
            "end_date": datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
            "organizer": "other organizer",
            "creator": admin_user,
            "title": "Event in IS",
            "pub_date": datetime.datetime.now(),
            "country": "IS",
            "geoposition": Geoposition(64.13244, -21.85690),
            "location": "Reykjavík",
            "audience": [1],
            "theme": [1],
            "tags": ["tag1", "tag2"],
        }

        event = create_or_update_event(**event_data)
        event.status = 'APPROVED'
        event.save()

        response_json = client.get('/api/scoreboard/?format=json')
        response_data = json.loads(response_json.content)

        assert isinstance(response_data, list)
        assert len(response_data) > 1
        assert response_data[0]["country_name"] == "Iceland"
        assert response_data[1]["country_name"] == "Slovenia"
