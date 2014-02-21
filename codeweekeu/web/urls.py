from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin
from web.views.events import EventListView,PendingListEventView

admin.autodiscover()

urlpatterns = patterns(
    'web.views',
    url(r'^$', 'events.index', name='web.index'),
    url(r'^add/$', 'events.add_event', name='web.add_event'),
    url(r'^view/(?P<event_id>\d+)/$', 'events.view_event', name='web.view_event'),
    url(r'^thankyou/$', 'events.thankyou', name='web.thankyou'),
)

urlpatterns+=patterns(
    '',
    url(r'^approved/(?P<country_code>\w{2,3})/$',EventListView.as_view(),name="web.list_events"),
    url(r'^pending/(?P<country_code>\w{2,3})/$', PendingListEventView.as_view(),name="web.pending_events"),
)