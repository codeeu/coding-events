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
from api.processors import get_created_events
from api.processors import get_next_or_previous
from api.processors import get_nearby_events
from web.forms.event_form import AddEventForm
from web.forms.event_form import SearchEventForm
from web.processors.event import get_initial_data
from web.processors.event import change_event_status
from web.processors.event import reject_event_status
from web.processors.event import create_or_update_event
from web.processors.user import update_user_email
from web.processors.user import get_ambassadors
from web.processors.event import get_client_ip
from web.processors.event import get_lat_lon_from_user_ip
from web.processors.event import list_countries
from web.processors.event import get_country
from web.processors.event import get_country_from_user_ip
from web.processors.event import count_approved_events_for_country
from web.processors.media import process_image
from web.processors.media import ImageSizeTooLargeException
from web.processors.media import UploadImageError
from web.decorators.events import can_edit_event
from web.decorators.events import can_moderate_event
from web.decorators.events import is_ambassador


"""
Do not Query the database directly from te view.
Use a processors file within the api app, put all of your queries there and
then call your newly created function in view!!! .-Erika
"""


def index(request):
	template = 'pages/index.html'

	past = request.GET.get('past', 'no')

	user_ip = get_client_ip(forwarded=request.META.get('HTTP_X_FORWARDED_FOR'),
	                        remote=request.META.get('REMOTE_ADDR'))
	country = get_country_from_user_ip(user_ip)

	try:
		lan_lon = get_lat_lon_from_user_ip(user_ip)
	except GeoIPException:
		lan_lon = (58.08695, 5.58121)
	
	ambassadors = get_ambassadors(country['country_code'])
	all_countries = list_countries()
	
	return render_to_response(
		template, {
			'lan_lon': lan_lon,
			'country': country,
			# all_countries minus two CUSTOM_COUNTRY_ENTRIES
			'all_countries': all_countries[2:],
			'past': past,
			'ambassadors': ambassadors,
		},
		context_instance=RequestContext(request))


@login_required
def add_event(request):
	if request.method == 'POST':
		event_form = AddEventForm(data=request.POST, files=request.FILES)

		if event_form.is_valid():
			picture = request.FILES.get('picture', None)
			event_data = {}
			try:
				if picture:
					if picture.size > (256 * 1024):
						raise ImageSizeTooLargeException('Image size too large.')

					event_data['picture'] = process_image(picture)

				event_data.update(event_form.cleaned_data)
				event_data['creator'] = request.user

				# checking if user entered a different email than in her profile
				if request.user.email != event_data['user_email']:
					update_user_email(request.user.id, event_data['user_email'])
				event_data.pop('user_email')

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
	else:
		event_form = AddEventForm(initial={'user_email': request.user.email})

	return render_to_response("pages/add_event.html", {
		'form': event_form,
	}, context_instance=RequestContext(request))


@login_required
@can_edit_event
def edit_event(request, event_id):
	event = get_event_by_id(event_id)
	user = request.user
	initial = get_initial_data(event)
	initial['user_email'] = request.user.email

	event_data = {}

	if request.method == 'POST':
		event_form = AddEventForm(data=request.POST, files=request.FILES)
	else:
		event_form = AddEventForm(initial=initial)

	existing_picture = event.picture
	
	if event_form.is_valid():
		# picture_check works with jasny bootstrap magix
		picture_check = request.POST.get('picture')
		picture = request.FILES.get('picture', None)
		event_data = event_form.cleaned_data
		event_data['creator'] = request.user

		# checking if user entered a different email than in her profile
		if user.email != event_data['user_email']:
			update_user_email(user.id, event_data['user_email'])
		event_data.pop('user_email')

		try:
			if picture:
				if picture.size > (256 * 1024):
					raise ImageSizeTooLargeException('Image size too large.')
				event_data['picture'] = process_image(picture)
			elif picture_check == "nochange":
				event_data['picture'] = existing_picture
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


def view_event(request, event_id, slug):
	event = get_event_by_id(event_id)
	next_event = get_next_or_previous(event, country_code=event.country)
	nearby = get_nearby_events(event, limit=4)

	return render_to_response(
		'pages/view_event.html', {
			'event': event,
			'next_event': next_event,
			'nearby': nearby
		}, context_instance=RequestContext(request))


@login_required
@is_ambassador
def list_pending_events(request, country_code):
	"""
	Display a list of pending events.
	"""

	active_page = request.GET.get('page','')

	if request.user.is_staff:
		event_list = get_pending_events(past=True)
		event_list = sorted(event_list, key=lambda a: a.country.code)
	else:
		event_list = get_pending_events(country_code=country_code, past=True)

	country_name = unicode(dict(countries)[country_code])

	return render_to_response(
		'pages/list_events.html', {
			'event_list': event_list,
			'status': 'pending',
			'country_code': country_code,
			'country_name': country_name,
			'active_page': active_page
		}, context_instance=RequestContext(request))


@login_required
@is_ambassador
def list_approved_events(request, country_code):
	"""
	Display a list of approved events.
	"""

	event_list = get_approved_events(country_code=country_code, past=True)

	country_name = unicode(dict(countries)[country_code])

	return render_to_response('pages/list_events.html', {
		'event_list': event_list,
		'status': 'approved',
		'country_code': country_code,
		'country_name': country_name
	}, context_instance=RequestContext(request))


@login_required
def created_events(request):
	"""
	Display a list of pending events.
	"""
	creator = request.user
	event_list = get_created_events(creator=creator, past=True)

	return render_to_response(
		'pages/list_user_events.html', {
			'event_list': event_list,
		}, context_instance=RequestContext(request))


def search_events(request):

		country_filter = request.GET.get('country_code', None)
		if not country_filter:
			user_ip = get_client_ip(forwarded=request.META.get('HTTP_X_FORWARDED_FOR'),
		                        remote=request.META.get('REMOTE_ADDR'))
			country = get_country(country_filter, user_ip)
			country_filter = country['country_code']

		past = request.GET.get('past_events', 'off')
		if past == 'on':
			past_events = True
		else:
			past_events = False

		search_query = request.GET.get('q', '')

		template = 'pages/search_events.html'
		page_template = 'pages/ajax_faceted_search_events.html'

		if request.method == 'POST':
			form = SearchEventForm(request.POST)

			if form.is_valid():
				search_filter = form.cleaned_data.get('q', None)
				country_filter = form.cleaned_data.get('country', None)
				theme_filter = form.cleaned_data.get('theme', None)
				audience_filter = form.cleaned_data.get('audience', None)
				past_events = form.cleaned_data.get('past_events',None)

				events = get_filtered_events(search_filter, country_filter, theme_filter, audience_filter, past_events)
		else:
			theme_filter = request.GET.getlist('theme', None)
			audience_filter =request.GET.getlist('audience', None)

			form = SearchEventForm(q=search_query, country_code=country_filter, past_events=past_events, audience=audience_filter, theme=theme_filter)
			events = get_filtered_events(search_query, country_filter, theme_filter, audience_filter, past_events)

		if request.is_ajax():
			return render_to_response(
				page_template, 
				{
					'events':events,
					'all_results': events.count(),
				},
				context_instance=RequestContext(request))

		return render_to_response(
			template,
			{
				'page_template': page_template,
				'events': events,
				'form': form,
				'country': country_filter,
				'all_results': events.count(),
			},
			context_instance=RequestContext(request))

def scoreboard(request):
	template = 'pages/scoreboard.html'

	counts = count_approved_events_for_country()
	
	return render_to_response(
		template, {
			'counts': counts,
		},
		context_instance=RequestContext(request))


@login_required
@can_moderate_event
def change_status(request, event_id):
	event = change_event_status(event_id)

	return HttpResponseRedirect(reverse('web.view_event', args=[event_id, event.slug]))

@login_required
@can_moderate_event
def reject_status(request, event_id):
	event = reject_event_status(event_id)

	return HttpResponseRedirect(reverse('web.view_event', args=[event_id, event.slug]))
