# -*- coding: utf-8 -*-
import pytest

@pytest.mark.django_db
def test_unknown_URL(db, client):
	response = client.get('/bar-foo/')

	assert response.status_code == 404
