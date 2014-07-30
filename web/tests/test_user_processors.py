import datetime
from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User, Group

from api.models.events import Event
from api.models import UserProfile
from web.processors.user import get_ambassadors_for_country


class EventTestCase(TestCase):
	
	def setUp(self):
		self.u1 = User.objects.create(username='user1')
		self.up1 = UserProfile.objects.create(user=self.u1)

		Event.objects.create(organizer="asdasd",
							 creator=User.objects.filter(pk=1)[0],
		                     title="asdasd",
		                     description="asdsad",
		                     location="asdsad",
		                     start_date=datetime.datetime.now(),
		                     end_date=datetime.datetime.now(),
		                     event_url="http://eee.com",
		                     contact_person="ss@ss.com",
		                     country="SI",
		                     audience=[1],
		                     theme=[1],		                     
		                     pub_date=datetime.datetime.now(),
		                     tags=["tag1", "tag2"])

	def test_get_ambassadors_for_country(self):
		self.up1.country = "SI"
		self.up1.save()

		group = Group.objects.get(name="ambassadors")

		group.user_set.add(self.u1)

		self.assertItemsEqual ([self.u1], get_ambassadors_for_country("SI"))
		self.assertItemsEqual ([], get_ambassadors_for_country("FR"))
