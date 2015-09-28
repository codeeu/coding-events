from django.test import TestCase
from django.contrib.auth.models import User, Group

from api.models import UserProfile
from web.processors.user import get_ambassadors_for_country


class EventTestCase(TestCase):

    def setUp(self):
        self.u1 = User.objects.create(username='user1')
        self.up1 = UserProfile.objects.create(user=self.u1)

    def test_get_ambassadors_for_country(self):
        self.up1.country = "SI"
        self.up1.save()

        group = Group.objects.get(name="ambassadors")

        group.user_set.add(self.u1)

        self.assertItemsEqual([self.u1], get_ambassadors_for_country("SI"))
        self.assertItemsEqual([], get_ambassadors_for_country("FR"))
