################################################
# Processors for events views
################################################
from django.conf import settings
from django.contrib.gis.geoip import GeoIP
from api.models import Event


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

def get_event(event_id):
	event = Event.objects.get(id=event_id)
	return event

def create_or_update_event(event_id=None, **event_data):
	"""
	Creates or updates Event object
	"""
	event = Event.objects.filter(id=event_id)
	if event:
		event = event[0]
		event_tags = []
		#we have to update tags after the other fields are updated
		if 'tags' in event_data:
			event_tags=event_data['tags']
			event_data.pop('tags')

		#in case we have geoposition data in event_data
		if 'geoposition' in event_data:
			# updating geoposition field is a bit fussy
			event_latitude = event_data['geoposition'][0]
			event_longitude = event_data['geoposition'][1]
			event_data.pop('geoposition')
			# updating all other fields
			event.__dict__.update(event_data)
			#setting new values for geoposition
			event.__dict__['geoposition'].latitude = event_latitude
			event.__dict__['geoposition'].longitude = event_longitude
			event.save()
		else:
			event.__dict__.update(event_data)
			event.save()

		#delete old tags and store new ones
		event.tags.set(*event_tags)

	else:
		event = Event.objects.create(**event_data)
	return event

