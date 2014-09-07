# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from api.views import EventListApi

urlpatterns = patterns('',
	url(r'^event/list/$', EventListApi.as_view(), name='event.list'),
)
