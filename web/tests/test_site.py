# -*- coding: utf-8 -*-
import pytest
import datetime

from web.processors.event import create_or_update_event

@pytest.mark.django_db
def test_unknown_URL(db, client):
	response = client.get('/bar-foo/')

	assert response.status_code == 404

@pytest.mark.django_db
def test_country_redirect(db, client):
	# Test without a slash in the end
	response = client.get('/AB')

	assert response.status_code == 301
	assert response['Location'][-5:] == '/#!AB'

	# and with one
	response = client.get('/AB/')

	assert response.status_code == 301
	assert response['Location'][-5:] == '/#!AB'

@pytest.mark.django_db
def test_view_just_id(admin_user, db, client):
	event_data = {
		'audience': [3],
		'theme': [1,2],
		'contact_person': u'test@example.com',
		'country': u'SI',
		'description': u'Lorem ipsum dolor sit amet',
		'event_url': u'',
		'location': u'Ljubljana, Slovenia',
		'organizer': u'CodeCatz test',
		"creator": admin_user,
		'start_date': datetime.datetime.now(),
		'end_date': datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
		'tags': [u'css', u'html', u'web'],
		'title': u'Redirect Test',
	}

	test_event = create_or_update_event(event_id=None, **event_data)

	# Test without a slash in the end
	response = client.get('/view/1')
	assert response.status_code == 301

	# Test with a slash in the end
	response = client.get('/view/1/')
	assert response.status_code == 302
