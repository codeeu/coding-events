import datetime
from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User

from api.models import Event
from api.models import EventTheme
from api.models import EventAudience
from api.models import UserProfile

from api.processors import get_all_events
from api.processors import get_pending_events
from api.processors import get_event_by_id
from api.processors import get_filtered_events

from web.tests import EventFactory, ApprovedEventFactory, PastEventFactory


class EventTestCase(TestCase):

    def setUp(self):
        self.u1 = User.objects.create(username='user1')
        self.up1 = UserProfile.objects.create(user=self.u1)

        self.creator = User.objects.filter(pk=1)[0]

        event = Event.objects.create(
            organizer='asdasd',
            creator=self.creator,
            title='asdasd',
            description='asdsad',
            location='asdsad',
            start_date=datetime.datetime.now() -
            datetime.timedelta(
                days=1,
                hours=3),
            end_date=datetime.datetime.now() +
            datetime.timedelta(
                days=3,
                hours=3),
            event_url='http://eee.com',
            contact_person='ss@ss.com',
            country='SI',
            pub_date=datetime.datetime.now())

        theme = EventTheme.objects.filter(pk=1)
        audience = EventAudience.objects.filter(pk=1)
        event.theme.add(*theme)
        event.audience.add(*audience)

    def test_get_all_events_with_one_event(self):
        all_events = get_all_events()
        self.assertEqual(1, all_events.count())

    def test_get_all_events_with_two_events(self):
        event = EventFactory.create()
        theme = EventTheme.objects.filter(pk=1)
        audience = EventAudience.objects.filter(pk=1)
        event.theme.add(*theme)
        event.audience.add(*audience)

        all_events = get_all_events()
        self.assertEqual(2, all_events.count())

    def test_get_all_events_with_different_statuses(self):
        event = ApprovedEventFactory.create()
        theme = EventTheme.objects.filter(pk=1)
        audience = EventAudience.objects.filter(pk=1)

        event.theme.add(*theme)
        event.audience.add(*audience)
        event.save()

        self.assertEqual('PENDING', get_event_by_id(1).status)
        self.assertEqual('APPROVED', event.status)

        all_events = get_all_events()
        self.assertEqual(2, all_events.count())

    def test_get_approved_events(self):
        test_event = Event.objects.get(title='asdasd')
        self.assertEqual('PENDING', test_event.status)
        test_event.status = 'APPROVED'
        test_event.save()
        self.assertEqual('APPROVED', test_event.status)

    def test_get_pending_events(self):
        pending = get_pending_events()
        self.assertEqual(1, pending.count())

    def test_get_pending_events_when_there_is_none(self):
        test_event = Event.objects.get(title='asdasd')
        test_event.status = 'APPROVED'
        test_event.save()
        self.assertFalse(get_pending_events().exists())

        test_event.delete()

    def test_get_pending_events_for_country(self):
        pending = get_pending_events(country_code='SI')
        self.assertEqual(1, pending.count())

    def test_get_pending_events_limit_to_one_ordered_by_location_desc(self):
        event = EventFactory.create(
            title='test_get_pending_events_limit_to_one_ordered_by_location_desc',
            location='invalid location')
        theme = EventTheme.objects.filter(pk=1)
        audience = EventAudience.objects.filter(pk=1)

        event.theme.add(*theme)
        event.audience.add(*audience)
        event.save()

        pending = get_pending_events(limit=1, order='-location')
        self.assertEquals(1, pending.count())
        self.assertEquals(
            'test_get_pending_events_limit_to_one_ordered_by_location_desc',
            pending[0].title)

    def test_get_event_by_id_without_id(self):
        with self.assertRaises(TypeError):
            get_event_by_id()

    def test_get_event_by_id_ok(self):
        test_event = get_event_by_id(1)
        self.assertEqual(1, test_event.pk)

    def test_get_filtered_events_with_no_search_filter(self):
        event = ApprovedEventFactory.create(
            title='test_get_filtered_events_with_no_search_filter')
        theme = EventTheme.objects.filter(pk=1)
        audience = EventAudience.objects.filter(pk=1)
        event.theme.add(*theme)
        event.audience.add(*audience)
        event.save()

        events = get_filtered_events()
        self.assertEquals(
            'test_get_filtered_events_with_no_search_filter',
            events[0].title)

        event.delete()

    def test_get_filtered_events_with_search_filter_when_no_aproved_event(
            self):
        search_filter = "asd"
        events = get_filtered_events(search_filter=search_filter)
        self.assertEquals(0, events.count())

    def test_get_filtered_events_with_country_filter_when_no_aproved_event(
            self):
        country_filter = "SI"
        events = get_filtered_events(country_filter=country_filter)
        self.assertEquals(0, events.count())

    def test_get_filtered_events_with_theme_filter_when_no_aproved_event(self):
        theme_filter = EventTheme.objects.filter(pk=1)
        events = get_filtered_events(theme_filter=theme_filter)
        self.assertEquals(0, events.count())

    def test_get_filtered_events_with_audience_filter_when_no_aproved_event(
            self):
        audience_filter = EventAudience.objects.filter(pk=1)
        events = get_filtered_events(audience_filter=audience_filter)
        self.assertEquals(0, events.count())

    def test_get_filtered_events_with_search_filter_with_approved_event(self):
        event = Event.objects.get(title='asdasd')
        event.status = 'APPROVED'
        event.save()

        search_filter = "asd"
        events = get_filtered_events(search_filter=search_filter)
        self.assertEquals(1, events.count())
        self.assertEquals('asdasd', events[0].title)

        event.delete()

    def test_get_filtered_events_with_search_filter_searching_title(self):
        event = ApprovedEventFactory.create(title='Programming for dummies')
        theme = EventTheme.objects.filter(pk=1)
        audience = EventAudience.objects.filter(pk=1)
        event.theme.add(*theme)
        event.audience.add(*audience)
        event.save()

        search_filter = "dummies"
        events = get_filtered_events(search_filter=search_filter)
        self.assertEquals(1, events.count())
        self.assertEquals('Programming for dummies', events[0].title)

        event.delete()

    def test_get_filtered_events_with_search_filter_searching_organizer(self):
        event = ApprovedEventFactory.create(organizer='CodeCatz')
        theme = EventTheme.objects.filter(pk=1)
        audience = EventAudience.objects.filter(pk=1)
        event.theme.add(*theme)
        event.audience.add(*audience)
        event.save()

        search_filter = "Catz"
        events = get_filtered_events(search_filter=search_filter)
        self.assertEquals(1, events.count())
        self.assertEquals('CodeCatz', events[0].organizer)

        event.delete()

    def test_get_filtered_events_with_search_filter_searching_description(
            self):
        event = ApprovedEventFactory(
            description='Learn basics about programming in python')
        theme = EventTheme.objects.filter(pk=1)
        audience = EventAudience.objects.filter(pk=1)
        event.theme.add(*theme)
        event.audience.add(*audience)
        event.save()

        search_filter = "python"
        events = get_filtered_events(search_filter=search_filter)
        self.assertEquals(1, events.count())
        self.assertEquals(2, events[0].pk)

        event.delete()

    def test_get_filtered_events_with_search_filter_searching_description_when_no_approved_event(
            self):
        event = EventFactory(
            description='Learn basics about programming in python')
        theme = EventTheme.objects.filter(pk=1)
        audience = EventAudience.objects.filter(pk=1)
        event.theme.add(*theme)
        event.audience.add(*audience)
        event.save()

        search_filter = "python"
        events = get_filtered_events(search_filter=search_filter)
        self.assertEquals(0, events.count())

        event.delete()

    def test_get_filtered_events_with_country_filter_with_approved_event(self):
        test_event = Event.objects.get(title='asdasd')
        test_event.status = 'APPROVED'
        test_event.save()
        country_filter = "SI"
        events = get_filtered_events(country_filter=country_filter)
        self.assertEquals(1, events.count())
        self.assertEquals('asdasd', events[0].title)

    def test_get_filtered_events_with_theme_filter_with_approved_event(self):
        test_event = Event.objects.get(title='asdasd')
        test_event.status = 'APPROVED'
        test_event.save()
        theme_filter = EventTheme.objects.filter(pk=1)
        events = get_filtered_events(theme_filter=theme_filter)
        self.assertEquals(1, events.count())
        self.assertEquals('asdasd', events[0].title)

    def test_get_filtered_events_with_audience_filter_with_approved_event(
            self):
        test_event = Event.objects.get(title='asdasd')
        test_event.status = 'APPROVED'
        test_event.save()
        audience_filter = EventAudience.objects.filter(pk=1)
        events = get_filtered_events(audience_filter=audience_filter)
        self.assertEquals(1, events.count())
        self.assertEquals('asdasd', events[0].title)

    def test_get_filtered_events_with_search_filter_and_theme_filter_with_approved_event(
            self):
        test_event = Event.objects.get(title='asdasd')
        test_event.status = 'APPROVED'
        test_event.save()
        search_filter = "asd"
        theme_filter = EventTheme.objects.filter(pk=1)
        events = get_filtered_events(
            search_filter=search_filter,
            theme_filter=theme_filter)
        self.assertEquals(1, events.count())
        self.assertEquals('asdasd', events[0].title)

    def test_get_filtered_events_with_search_filter_and_country_filter_with_approved_event(
            self):
        test_event = Event.objects.get(title='asdasd')
        test_event.status = 'APPROVED'
        test_event.save()
        search_filter = "asd"
        country_filter = "SI"

        events = get_filtered_events(
            search_filter=search_filter,
            country_filter=country_filter)
        self.assertEquals(1, events.count())
        self.assertEquals('asdasd', events[0].title)

    def test_get_filtered_events_with_theme_filter_and_audience_filter_with_more_approved_event(
            self):
        event = ApprovedEventFactory.create()
        theme = EventTheme.objects.filter(pk=1)
        audience = EventAudience.objects.filter(pk=1)
        event.theme.add(*theme)
        event.audience.add(*audience)
        event.save()

        test_event = Event.objects.get(title='asdasd')
        test_event.status = 'APPROVED'
        test_event.save()
        theme_filter = EventTheme.objects.filter(pk=1)
        audience_filter = EventAudience.objects.filter(pk=1)
        events = get_filtered_events(
            theme_filter=theme_filter,
            audience_filter=audience_filter)
        self.assertEquals(2, events.count())

    def test_get_filtered_events_with_theme_filter_and_audience_filter_with_past_approved_events(
            self):
        event = ApprovedEventFactory.create(title='Programming for dummies')
        theme = EventTheme.objects.filter(pk=1)
        audience = EventAudience.objects.filter(pk=1)
        event.theme.add(*theme)
        event.audience.add(*audience)
        event.save()

        test_event = Event.objects.get(title='asdasd')
        test_event.status = 'APPROVED'
        test_event.save()

        theme_filter = EventTheme.objects.filter(pk=1)
        audience_filter = EventAudience.objects.filter(pk=1)
        events = get_filtered_events(
            theme_filter=theme_filter,
            audience_filter=audience_filter,
            past_events=True)
        self.assertEquals(2, events.count())

        event.delete()

    def test_get_filtered_events_with_search_filter_searching_description_and_past_events(
            self):
        event = PastEventFactory.create(
            description='Learn basics about programming in python',
            status='APPROVED')

        theme = EventTheme.objects.filter(pk=1)
        audience = EventAudience.objects.filter(pk=1)
        event.theme.add(*theme)
        event.audience.add(*audience)
        event.save()

        search_filter = "python"
        events = get_filtered_events(
            search_filter=search_filter, past_events=True)
        self.assertEquals(1, events.count())
        self.assertEquals(2, events[0].pk)

    def test_get_filtered_events_with_search_filter_and_more_past_approved_events(
            self):
        event = PastEventFactory.create(
            title='Programming for dummies asdasd',
            status='APPROVED')

        theme = EventTheme.objects.filter(pk=1)
        audience = EventAudience.objects.filter(pk=1)
        event.theme.add(*theme)
        event.audience.add(*audience)
        event.save()

        test_event = Event.objects.get(title='asdasd')
        test_event.status = 'APPROVED'
        test_event.save()
        search_filter = "asdasd"
        events = get_filtered_events(
            search_filter=search_filter, past_events=True)
        self.assertEquals(2, events.count())

    def test_event_with_empty_slug(self):
        event = EventFactory.create(title='#^^#')

        assert event.title == '#^^#'
        assert event.slug != ''
        assert event.slug == 'event'
