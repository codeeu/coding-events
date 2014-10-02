# -*- coding: utf-8 -*-
import pytest

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
