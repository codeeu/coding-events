import json
from django.contrib.gis.geoip import GeoIPException
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import loader
from django.template import Context
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers
from django.core.urlresolvers import reverse
from django_countries import countries

from api.processors import get_event_by_id
from api.processors import get_filtered_events
from api.processors import get_approved_events
from api.processors import get_pending_events
from web.forms.event_form import AddEventForm
from web.forms.event_form import SearchEventForm
from web.processors.event import get_initial_data
from web.processors.event import change_event_status
from web.processors.event import create_or_update_event
from web.processors.event import get_client_ip
from web.processors.event import get_lat_lon_from_user_ip
from web.processors.event import get_country_from_user_ip
from web.processors.event import list_countries
from web.processors.media import process_image
from web.processors.media import ImageSizeTooLargeException
from web.processors.media import UploadImageError
from web.decorators.events import can_edit_event

"""
Do not Query the database directly from te view.
Use a processors file within the api app, put all of your queries there and
then call your newly created function in view!!! .-Erika
"""


def index(request, country_code=None):
	template = 'pages/index.html'
	events = get_approved_events()
	map_events = serializers.serialize('json', events, fields=('geoposition', 'title', 'pk', 'slug'))

	user_ip = get_client_ip(forwarded=request.META.get('HTTP_X_FORWARDED_FOR'),
	                        remote=request.META.get('REMOTE_ADDR'))

	if country_code and 'media' not in country_code:
		country_name = unicode(dict(countries)[country_code])
		country = {'country_name': country_name, 'country_code': country_code}
	else:
		country = get_country_from_user_ip(user_ip)

	if request.is_ajax():
		if request.META.get('HTTP_X_PJAX', None):
			template = 'pages/pjax_index.html'
		else:
			template = 'layout/all_events.html'

	try:
		lan_lon = get_lat_lon_from_user_ip(user_ip)
	except GeoIPException:
		lan_lon = (46.0608144, 14.497165600000017)

	events = get_approved_events(order='pub_date', country_code=country.get('country_code', None))

	all_countries = list_countries()
	return render_to_response(
		template, {
			'latest_events': events,
			'map_events': map_events,
			'lan_lon': lan_lon,
			'country': country,
			'all_countries': all_countries,
		},
		context_instance=RequestContext(request))


@login_required
def add_event(request):
	event_form = AddEventForm()

	if request.method == 'POST':
		event_form = AddEventForm(data=request.POST, files=request.FILES)

	if event_form.is_valid():
		picture = request.FILES.get('picture')

		try:
			if picture:
				if picture.size > (256 * 1024):
					raise ImageSizeTooLargeException('Image size too large.')

				process_image(picture)

			event_data = {}
			event_data.update(event_form.cleaned_data)
			event = create_or_update_event(**event_data)

			t = loader.get_template('alerts/thank_you.html')
			c = Context({'event': event, })
			messages.info(request, t.render(c))

			return HttpResponseRedirect(reverse('web.view_event', args=[event.pk, event.slug]))

		except ImageSizeTooLargeException:
			messages.error(request, 'The image is just a bit too big for us. '
			                        'Please reduce your image size and try agin.')
		except UploadImageError as e:
			messages.error(request, e.message)

	return render_to_response("pages/add_event.html", {
		'form': event_form,
	}, context_instance=RequestContext(request))


@login_required
@can_edit_event
def edit_event(request, event_id):
	event = get_event_by_id(event_id)
	initial = get_initial_data(event)

	event_data = {}

	if request.method == 'POST':
		event_form = AddEventForm(data=request.POST, files=request.FILES)
	else:
		event_form = AddEventForm(initial=initial)

	if event_form.is_valid():
		picture = request.FILES.get('picture', None)
		event_data = event_form.cleaned_data

		try:
			if picture:
				if picture.size > (256 * 1024):
					raise ImageSizeTooLargeException('Image size too large.')

				process_image(picture)
			else:
				del event_data['picture']

			create_or_update_event(event_id, **event_data)

			return HttpResponseRedirect(reverse('web.view_event',
			                                    kwargs={'event_id': event.id, 'slug': event.slug}))

		except ImageSizeTooLargeException:
			messages.error(request, 'The image is just a bit too big for us (must be up to 256 kb). '
			                        'Please reduce your image size and try agin.')
		except UploadImageError as e:
			messages.error(request, e.message)

	return render_to_response(
		'pages/add_event.html', {
			'form': event_form,
			'address': event_data.get('location', None),
			'editing': True,
			'picture_url': event.picture,
		}, context_instance=RequestContext(request))


def view_event_by_country(request, country_code):
	event_list = get_approved_events(country_code=country_code)

	return render_to_response(
		'pages/list_events.html', {
			'event_list': event_list,
		}, context_instance=RequestContext(request))


def view_event(request, event_id, slug):
	event = get_event_by_id(event_id)

	return render_to_response(
		'pages/view_event.html', {
			'event': event,
		}, context_instance=RequestContext(request))


@login_required
def list_pending_events(request, country_code):
	"""
	Display a list of pending events.
	"""

	event_list = get_pending_events(country_code=country_code)

	return render_to_response(
		'pages/list_events.html', {
			'event_list': event_list,
			'status': 'pending',
			'country_code': country_code,
		}, context_instance=RequestContext(request))


@login_required
def list_approved_events(request, country_code):
	"""
	Display a list of approved events.
	"""

	event_list = get_approved_events(country_code=country_code)

	return render_to_response('pages/list_events.html', {
		'event_list': event_list,
		'status': 'approved',
		'country_code': country_code
	}, context_instance=RequestContext(request))


def search_events(request):
		user_ip = get_client_ip(forwarded=request.META.get('HTTP_X_FORWARDED_FOR'),
		                        remote=request.META.get('REMOTE_ADDR'))
		country = get_country_from_user_ip(user_ip)
		events = get_approved_events(country_code=country)

		if request.method == 'POST':
			form = SearchEventForm(request.POST)

			if form.is_valid():
				search_filter = form.cleaned_data.get('search', None)
				country_filter = form.cleaned_data.get('country', None)
				theme_filter = form.cleaned_data.get('theme', None)
				audience_filter = form.cleaned_data.get('audience', None)

				events = get_filtered_events(search_filter, country_filter, theme_filter, audience_filter)
		else:
			form = SearchEventForm()
			events = get_approved_events(country_code=country['country_code'])

		return render_to_response(
			'pages/search_events.html', {
				'events': events,
				'form': form,
			}, context_instance=RequestContext(request))


@login_required
@can_edit_event
def change_status(request, event_id):
	event = change_event_status(event_id)

	return HttpResponseRedirect(reverse('web.view_event', args=[event_id, event.slug]))
