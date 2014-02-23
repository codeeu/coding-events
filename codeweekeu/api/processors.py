from models.events import Event


def get_all_events():
	return Event.objects.all()


def get_event_by_id(event_id):
	event = Event.objects.get(id=event_id)
	return event


def get_approved_events(limit=None, order=None):
	"""
	Select all events which are approved and optionaly limit and/or order them
	"""

	events = Event.objects.filter(status='APPROVED')

	if order:
		events.order_by(order)
	if limit:
		events = events[:limit]


	return events