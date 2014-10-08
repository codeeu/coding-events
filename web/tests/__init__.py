import factory
import datetime

from django.contrib.auth.models import User

from api.models.events import Event

class EventFactory(factory.DjangoModelFactory):
	class Meta:
		model = Event

	organizer="Event Organizer"
	creator=factory.LazyAttribute(lambda n: User.objects.get_or_create(username='test_user')[0])
	title="My Coding Event"
	description="Some description"
	location="Nonexisting location"

	event_url="http://example.com"
	contact_person="contact@example.com"
	country="SI"
	tags=["tag1", "tag2"]

	start_date=factory.LazyAttribute(lambda n: datetime.datetime.now() + datetime.timedelta(days=1, hours=3) )
	end_date=factory.LazyAttribute(lambda n: datetime.datetime.now() + datetime.timedelta(days=3, hours=3) )


class ApprovedEventFactory(EventFactory):
	status = "APPROVED"

class PastEventFactory(EventFactory):
	start_date = factory.LazyAttribute(lambda n: datetime.datetime.now() - datetime.timedelta(days=3, hours=3))
	end_date = factory.LazyAttribute(lambda n: datetime.datetime.now() - datetime.timedelta(days=1, hours=3) )