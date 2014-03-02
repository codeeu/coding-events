from django.contrib.gis.geoip import GeoIP
from api.models import Event

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
		event = Event.objects.create(**event_data)
	return event

