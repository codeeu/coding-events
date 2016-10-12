# -*- coding: utf-8 -*-
from hashlib import sha1

from rest_framework import generics
from rest_framework_extensions.cache.decorators import cache_response

from api.serializers import EventListSerializers
from api.processors import get_approved_events

from api.serializers import ScoreboardSerializer
from web.processors.event import count_approved_events_for_country


class CachedListAPIView(generics.ListAPIView):
    """
    Concrete cached view for listing a queryset.
    """
    @cache_response(timeout=21600, key_func='calculate_cache_key')
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def calculate_cache_key(self, view_instance, view_method, request, args, kwargs):
        return sha1('-'.join([
                repr(request.GET),
                repr(args),
                repr(kwargs),
            ])).hexdigest()


class EventListApi(CachedListAPIView):
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


class ScoreBoardApi(CachedListAPIView):
    "Lists scoreboard entries"
    serializer_class = ScoreboardSerializer

    def get_queryset(self):
        return count_approved_events_for_country()
