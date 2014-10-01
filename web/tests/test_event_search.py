# -*- coding: utf-8 -*-
import pytest

from web.tests import EventFactory, ApprovedEventFactory, PastEventFactory

@pytest.mark.django_db
def test_search_show_only_approved(db, client):
	approved_event = ApprovedEventFactory.create()
	unapproved_event = EventFactory.create()

	response = client.get('/search/')

	assert approved_event.get_absolute_url() in response.content
	assert unapproved_event.get_absolute_url() not in response.content

	map(lambda x: x.delete(), [approved_event, unapproved_event])

def test_search_do_not_show_past_events(db, client):
	future_event = ApprovedEventFactory.create()
	past_event = PastEventFactory.create(status='APPROVED')

	response = client.get('/search/')

	assert future_event.get_absolute_url() in response.content
	assert past_event.get_absolute_url() not in response.content

	map(lambda x: x.delete(), [future_event, past_event])

def test_search_show_past_events(db, client):
	future_event = ApprovedEventFactory.create()
	past_event = PastEventFactory.create(status='APPROVED')

	response = client.get('/search/?past=on')

	assert future_event.get_absolute_url() in response.content
	assert past_event.get_absolute_url() in response.content

	map(lambda x: x.delete(), [future_event, past_event])