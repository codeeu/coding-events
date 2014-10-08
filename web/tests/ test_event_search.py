# -*- coding: utf-8 -*-
import pytest
from django.core.urlresolvers import reverse

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


def test_search_events_with_search_query_all_countries_multiple_results(db, client):
	approved1 = ApprovedEventFactory.create(title="Event Arglebargle - Approved", country="SI")
	approved2 = ApprovedEventFactory.create(title="Event Arglebargle - Approved", country="AT")

	response = client.get(reverse('web.search_events'), {'q':'arglebargle', 'country':'00'}, REMOTE_ADDR='93.103.53.11')

	assert approved1.get_absolute_url() in response.content
	assert approved2.get_absolute_url() in response.content

	map(lambda x: x.delete(), [approved1, approved2])


def test_search_events_with_search_query(db, client):
	approved1 = ApprovedEventFactory.create(title='Event Arglebargle - Approved')
	response = client.get(reverse('web.search_events'), {'q':'arglebargle'}, REMOTE_ADDR='93.103.53.11')

	assert approved1.get_absolute_url() in response.content

	approved1.delete()



def test_search_events_with_unicode_tag_in_search_query(db, client):
	approved1 = ApprovedEventFactory.create(tags=[u"jabolčna čežana",u"José", "Django"])
	response = client.get(reverse('web.search_events'), {'q':'čežana'}, REMOTE_ADDR='93.103.53.11')

	assert approved1.get_absolute_url() in response.content

	approved1.delete()


def test_search_events_with_search_query_multiple_events_current_country_only(db, client):
	approved1 = ApprovedEventFactory.create(title="Event Arglebargle - Approved", country="SI")
	approved2 = ApprovedEventFactory.create(title="Event Arglebargle - Approved", country="AT")

	response = client.get(reverse('web.search_events'), {'q':'arglebargle'}, REMOTE_ADDR='93.103.53.11')

	assert approved1.get_absolute_url() in response.content
	assert approved2.get_absolute_url() not in response.content

	map(lambda x: x.delete(), [approved1, approved2])


def test_search_with_audience(db, client):
	approved1 = ApprovedEventFactory.create(title="Event Arglebargle - Approved", country="SI")
	response = client.get(reverse('web.search_events'), {'audience':1}, REMOTE_ADDR='93.103.53.11')

	assert approved1.get_absolute_url() in response.content

	approved1.delete()


def test_search_with_audience_multiple_events(db, client):
	approved1 = ApprovedEventFactory.create(title="Event Arglebargle - Approved", country="SI") #default audience 1
	approved2 = ApprovedEventFactory.create(title="Event Arglebargle - Approved", country="SI", audience=[1,2])
	approved3 = ApprovedEventFactory.create(title="Event Arglebargle - Approved", country="AT", audience=[1,2])
	approved4 = ApprovedEventFactory.create(title="Event Arglebargle - Approved", country="SI", audience=[3])
	response = client.get(reverse('web.search_events'), {'audience':1}, REMOTE_ADDR='93.103.53.11')

	assert approved1.get_absolute_url() in response.content
	assert approved2.get_absolute_url() in response.content
	assert approved3.get_absolute_url() not in response.content
	assert approved4.get_absolute_url() not in response.content

	map(lambda x: x.delete(), [approved1, approved2, approved3, approved4])



def test_search_with_theme(db, client):
	approved1 = ApprovedEventFactory.create(title="Event Arglebargle - Approved", country="SI", theme=[2])
	response = client.get(reverse('web.search_events'), {'theme':2}, REMOTE_ADDR='93.103.53.11')

	assert approved1.get_absolute_url() in response.content

	approved1.delete()


def test_search_with_theme_multiple_events(db, client):
	approved1 = ApprovedEventFactory.create(title="Event Arglebargle - Approved", country="SI")
	approved2 = ApprovedEventFactory.create(title="Event Arglebargle - Approved", country="SI", theme=[2])
	response = client.get(reverse('web.search_events'), {'theme':1}, REMOTE_ADDR='93.103.53.11')

	assert approved1.get_absolute_url() in response.content
	assert approved2.get_absolute_url() not in response.content

	map(lambda x: x.delete(), [approved1, approved2])



def test_search_with_theme_multiple_events_all_countries(db, client):
	approved1 = ApprovedEventFactory.create(title="Event Arglebargle - Approved", country="SI")
	approved2 = ApprovedEventFactory.create(title="Event Arglebargle - Approved", country="AT")
	response = client.get(reverse('web.search_events'), {'country':'00', 'theme':1}, REMOTE_ADDR='93.103.53.11')

	assert approved1.get_absolute_url() in response.content
	assert approved2.get_absolute_url() in response.content

	map(lambda x: x.delete(), [approved1, approved2])