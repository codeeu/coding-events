from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator


from api.models import Event
from web.forms.event_form import AddEvent
from web.processors.event import create_or_update_event, get_event
from web.processors.event import has_model_permissions



def index(request):
	latest_events = Event.approved.order_by('created')[:5]
	return render_to_response(
		'pages/index.html',
		{'events': latest_events},
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
