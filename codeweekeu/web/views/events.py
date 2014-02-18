from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from api.models import Event
from web.forms.event_form import AddEvent
from web.processors.event import create_or_update_event, get_event

def index(request):
	return render_to_response(
		'pages/index.html',
		{'test': 'test'},
		context_instance=RequestContext(request))

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
					{'title': event.title, 'event_id': event.id},
					context_instance=RequestContext(request))
	context = {"form": event_form}
	return render_to_response("pages/add_event.html", context, context_instance=RequestContext(request))

def view_event(request, event_id):
	event = get_object_or_404(Event, pk=event_id)
	context = {'event': event}
	return render_to_response("pages/view_event.html", context, context_instance=RequestContext(request))

def search_event(request):
	pass

def thankyou(request):
	return render_to_response('pages/thankyou.html')
