# -*- coding: utf-8 -*-
from rest_framework import generics

from api.serializers import EventListSerializers
from api.processors import get_approved_events

class EventListApi(generics.ListAPIView):
	""" Lists approved Events, takes the following optional GET parameters:

* limit
* order
* country_code
* past
	"""
	serializer_class = EventListSerializers

	def get_queryset(self):
		params = {
			'limit': self.request.GET.get('limit', None),
			'order': self.request.GET.get('order', None),
			'country_code': self.request.GET.get('country_code', None),
			'past': self.request.GET.get('past', False)
		}
		
		return get_approved_events(**params)

