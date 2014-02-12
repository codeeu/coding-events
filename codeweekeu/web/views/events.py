from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):

	return render_to_response(
		'pages/index.html',
		{'test': 'test'},
		context_instance=RequestContext(request))

def add_event(request):
	pass

def view_event(request):
	pass

def search_event(request):
	pass
