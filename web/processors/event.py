################################################
# Processors for events views
################################################
from django.conf import settings
from django.contrib.gis.geoip import GeoIP
from api.models import Event
from django_countries import countries

from web.processors import media


def get_client_ip(forwarded=None, remote=None):

	if settings.DEBUG:
		return '93.103.53.11'

	if forwarded:
		return forwarded.split(',')[0]
	return remote


def get_lat_lon_from_user_ip(ip):
	"""
	Return latitude and longitude of IP
	"""
	g = GeoIP()
	return g.lat_lon(ip)


def get_country_from_user_ip(ip):
	"""
	Return country of IP
	"""
	g = GeoIP()
	return g.country(ip)


def list_countries():
	all_countries = []
	for code, name in list(countries):
		readable_name = unicode(name)
		all_countries.append((readable_name, code))
	all_countries.sort()
	return all_countries


def get_initial_data(event):
	"""
	Processing event to fill in form data
	"""
	initial = event.__dict__
	initial['tags'] = event.get_tags()
	initial['audience'] = event.get_audience_array()
	initial['theme'] = event.get_theme_array()
	return initial


def create_or_update_event(event_id=None, **event_data):
	"""
	Creates or updates Event object
	"""
	event = Event.objects.filter(id=event_id)
	if event:
		event = event[0]
		# many to many fields have to updated after other fields are updated
		new_audiences = event_data['audience']
		del event_data['audience']
		new_themes = event_data['theme']
		del event_data['theme']
		event_tags = event_data['tags']
		del event_data['tags']

		#in case we have geoposition data in event_data
		if 'geoposition' in event_data:
			# updating geoposition field is a bit fussy
			event_latitude = event_data['geoposition'][0]
			event_longitude = event_data['geoposition'][1]
			del event_data['geoposition']
			# updating all other fields
			event.__dict__.update(event_data)
			#setting new values for geoposition
			event.__dict__['geoposition'].latitude = event_latitude
			event.__dict__['geoposition'].longitude = event_longitude
		else:
			event.__dict__.update(event_data)

		event.save()

		#delete old categories and tags and store new ones
		event.audience.clear()
		event.audience.add(*new_audiences)
		event.theme.clear()
		event.theme.add(*new_themes)
		event.tags.set(*event_tags)

	else:
		event = Event.objects.create(**event_data)
	return event


def change_event_status(event_id):
	event = Event.objects.get(pk=event_id)

	if event.status == 'APPROVED':
		event.status = 'PENDING'
	else:
		event.status = 'APPROVED'

	event.save()
	return event

