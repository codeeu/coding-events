import datetime
from django.db.models import Q
from models.events import Event
from models.events import EventTheme
from models.events import EventAudience


def get_all_events():
	return Event.objects.all()


def get_event_by_id(event_id):
	event = Event.objects.get(id=event_id)
	return event


def get_approved_events(limit=None, order=None, country_code=None, past=False):
	"""
	Select all events which are approved and optionally limit and/or order them
	"""

	events = Event.objects.filter(status='APPROVED')

	if not past:
		events = events.filter(end_date__gte=datetime.datetime.now())
	if country_code:
		events = events.filter(country=country_code)
	if order:
		events = events.order_by(order)
	if limit:
		events = events[:limit]
	
	return events


def get_pending_events(limit=None, order=None, country_code=None, past=False):

	"""
	Select all future or past events which are pending and optionally limit and/or order them
	"""

	events = Event.objects.filter(status='PENDING')
	if not past:
		events = events.filter(end_date__gte=datetime.datetime.now())
	if country_code:
		events = events.filter(country=country_code)
	if order:
		events = events.order_by(order)
	if limit:
		events = events[:limit]
	return events


def get_filtered_events(search_filter=None, country_filter=None, theme_filter=None, audience_filter=None):

	"""
	Filter events by given filter
	"""
	filter_args = ()

	# default
	filter_kwargs = {'status': 'APPROVED', 'end_date__gte': datetime.datetime.now()}

	if search_filter:
		filter_args = (Q(title__icontains=search_filter) | Q(description__icontains=search_filter) | Q(tags__name__icontains=search_filter) 
			| Q(organizer__icontains=search_filter) | Q(location__icontains=search_filter),)

	if country_filter:
		filter_kwargs['country'] = country_filter

	if theme_filter:
		filter_kwargs['theme__in'] = theme_filter

	if audience_filter:
		audience = EventAudience.objects.filter()
		filter_kwargs['audience__in'] = audience_filter

	if len(filter_args) > 0:
		events = Event.objects.filter(*filter_args, **filter_kwargs).distinct()
	else:
		events = Event.objects.filter(**filter_kwargs).distinct()

	return events

def get_created_events(creator, limit=None, order=None, country_code=None, past=False):

	"""
	Select all future or past events which are created by user and optionally limit and/or order them
	"""

	events = Event.objects.filter(creator=creator)
	if not past:
		events = events.filter(end_date__gte=datetime.datetime.now())
	if country_code:
		events = events.filter(country=country_code)
	if order:
		events = events.order_by(order)
	if limit:
		events = events = events[:limit]
	return events

def list_themes():
	themes = EventTheme.objects.all()

	return themes