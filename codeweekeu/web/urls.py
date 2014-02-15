from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'web.views',
    url(r'^$', 'events.index', name='web.index'),
    url(r'^add/$', 'events.add_event', name='events.add_event'),
    url(r'^thankyou/$', 'events.thankyou', name='events.thankyou'),
)