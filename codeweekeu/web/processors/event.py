from api.models import Event, CountryList

def get_event(event_id):
    event = Event.objects.get(id=event_id)
    return event

def create_or_update_event(event_id=None,**event_data):

    """
        Creates or updates Event object
    """
    event = Event.objects.filter(id=event_id)
    if event:
        event = event[0]
        event.__dict__.update(event_data)
        event.save()
    else:
        event = Event.objects.create(**event_data)
    return event
