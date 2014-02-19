from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'web.views',
    url(r'^$', 'events.index', name='web.index'),
    url(r'^add/$', 'events.add_event', name='web.add_event'),
    url(r'^view/(?P<event_id>\d+)/$', 'events.view_event', name='web.view_event'),
    url(r'^thankyou/$', 'events.thankyou', name='web.thankyou'),
    url(r'^help/$', 'events.help', name='web.help'),
)