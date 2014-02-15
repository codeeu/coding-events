from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from web.forms.event_form import AddEvent

def index(request):
	return render_to_response(
		'pages/index.html',
		{'test': 'test'},
		context_instance=RequestContext(request))

def add_event(request):
	event_form = AddEvent()
	if request.method =="POST":
		event_form = AddEvent(data=request.POST)
		if event_form.is_valid():
			return HttpResponseRedirect('/thankyou/')
	context = {"form": event_form}
	return render_to_response("pages/add_event.html", context, context_instance=RequestContext(request))

def view_event(request):
	pass

def search_event(request):
	pass

def thankyou(request):
	return render_to_response('pages/thankyou.html')
