# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from api.views import EventListApi
from api.views import ScoreBoardApi

urlpatterns = patterns('',
                       url(r'^event/list/$',
                           EventListApi.as_view(),
                           name='event.list'),
                       url(r'^scoreboard/$',
                           ScoreBoardApi.as_view(),
                           name='scoreboard'),
                       )
