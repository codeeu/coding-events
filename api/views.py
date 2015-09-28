# -*- coding: utf-8 -*-
from rest_framework import generics

from api.serializers import EventListSerializers
from api.processors import get_approved_events

from api.serializers import ScoreboardSerializer
from web.processors.event import count_approved_events_for_country


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


class ScoreBoardApi(generics.ListAPIView):
    "Lists scoreboard entries"
    serializer_class = ScoreboardSerializer

    def get_queryset(self):
        return count_approved_events_for_country()
