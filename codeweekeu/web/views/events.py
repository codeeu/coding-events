from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.core import serializers
from django.conf import settings

from api.models import Event
from web.forms.event_form import AddEvent
from web.processors.event import create_or_update_event
from web.processors.event import has_model_permissions
from web.processors.event import get_lat_lon_from_user_ip
from api.processors import get_approved_events

"""
Do not Query the database directly from te view.
Use a processors file within the api app, put all of your queries there and
then call your newly created function in view!!! .-Erika
"""


def index(request):
	events = get_approved_events()
	map_events = serializers.serialize('json', events, fields=('geoposition', 'title', 'pk', 'slug'))
	latest_events = get_approved_events(limit=5, order='pub_date')

	lan_lon = get_lat_lon_from_user_ip(get_client_ip(request))

	return render_to_response(
		'pages/index.html', {
			'latest_events': latest_events,
		    'map_events': map_events,
		    'lan_lon': lan_lon,
		},
		context_instance=RequestContext(request))


@login_required
def add_event(request):
	event_form = AddEvent()
	if request.method =="POST":
		event_form = AddEvent(data=request.POST, files=request.FILES)
		if event_form.is_valid():
			event_data = {}
			event_data.update(event_form.cleaned_data)
			event = create_or_update_event(**event_data)
			return render_to_response(
					'pages/thankyou.html',
					{'title': event.title, 'event_id': event.id, 'slug': event.slug},
					context_instance=RequestContext(request))
	context = {"form": event_form}
	return render_to_response("pages/add_event.html", context, context_instance=RequestContext(request))

def view_event(request, event_id, slug):
	event = get_object_or_404(Event, pk=event_id, slug=slug)
	context = {'event': event}
	return render_to_response("pages/view_event.html", context, context_instance=RequestContext(request))

def search_event(request):
	pass

def thankyou(request):
	return render_to_response('pages/thankyou.html')


class PendingListEventView(ListView):
	'''
		Display a list of pending events.
	'''
	model=Event
	template_name ="pages/list_events.html"
	queryset = Event.pending.all()

	#@method_decorator(login_required)--- we have to uncomment that before going live
	def dispatch(self, *args, **kwargs):
		return super(PendingListEventView,self).dispatch(*args, **kwargs)

	def get_queryset(self):
		return self.queryset.filter(country=self.kwargs["country_code"])

	def get(self,*args,**kwargs):
		if has_model_permissions(self.request.user,Event,["edit","submit","reject"],Event._meta.app_label):
			return super(PendingListEventView,self).get(*args, **kwargs)
		else:
			return HttpResponse("You don't have permissions to see this page")



class EventListView(ListView):

	model = Event
	template_name ="pages/list_events.html"
	queryset = Event.approved.all()

	def get_queryset(self):
		return self.queryset.filter(country=self.kwargs["country_code"])



def guide(request):
	return render_to_response('pages/guide.html')


def get_client_ip(request):
	if settings.DEBUG:
		return '93.103.53.11'

	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip
