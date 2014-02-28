__author__ = 'svetka'

from django.contrib.formtools.preview import FormPreview
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from web.processors.event import create_or_update_event

AUTO_ID = "id_%s"

class AddEventFormPreview(FormPreview):

	form_template = 'pages/add_event.html'
	preview_template = 'pages/preview_add_event.html'


	def get_auto_id(self):
		return AUTO_ID

	def done(self, request, cleaned_data):
		print "hello from done"
		event_data={}
		event_data.update(cleaned_data)
		event = create_or_update_event(**event_data)
		kwargs={'event_id': event.id, 'slug': event.slug}
		return HttpResponseRedirect(reverse("web.view_event", kwargs=kwargs))





