# coding=utf-8

import datetime
import pytest
import StringIO
import os

from py.path import local
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User, Group

from api.models.events import Event
from api.models import UserProfile

from avatar.models import Avatar
from avatar.util import get_primary_avatar

from web.processors.event import create_or_update_event
from web.processors.event import count_approved_events_for_country

from web.tests import EventFactory, ApprovedEventFactory


class EventViewsTestCase(TestCase):

    def setUp(self):
        self.u1 = User.objects.create(username='user1')
        self.up1 = UserProfile.objects.create(user=self.u1)

        pending = Event.objects.create(
            organizer="Organizer 1",
            creator=User.objects.filter(
                pk=1)[0],
            title="Event 1 - Pending",
            description="Some description - Pending",
            location="Near here",
            start_date=datetime.datetime.now() +
            datetime.timedelta(
                days=1,
                hours=3),
            end_date=datetime.datetime.now() +
            datetime.timedelta(
                days=3,
                hours=3),
            event_url="http://eee.com",
            contact_person="ss@ss.com",
            country="SI",
            pub_date=datetime.datetime.now(),
            tags=[
                    "tag1",
                "tag2"])

        client = Client()

    def test_index_view_without_approved_events(self):
        response = self.client.get(
            reverse('web.index'), {}, REMOTE_ADDR='93.103.53.11')

        self.assertEquals(200, response.status_code)
        self.assertEquals((46.0, 15.0), response.context['lan_lon'])
        self.assertEquals('SI', response.context['country']['country_code'])
        self.assertTemplateUsed(response, 'pages/index.html')

    def test_index_view_changing_remote_in_request(self):
        # setup
        response = self.client.get(
            reverse('web.index'),
            {},
            HTTP_X_FORWARDED_FOR='93.103.53.11, 93.103.53.11')

        # assert
        self.assertEquals(200, response.status_code)
        self.assertEquals((46.0, 15.0), response.context['lan_lon'])

    def test_search_events_with_search_query(self):
        ApprovedEventFactory.create(title='Event Arglebargle - Approved')
        response = self.client.get(
            reverse('web.search_events'), {
                'q': 'arglebargle'}, REMOTE_ADDR='93.103.53.11')

        self.assertEquals(1, response.context['events'].count())
        self.assertEquals('SI', response.context['country'])

    def test_search_events_with_unicode_tag_in_search_query(self):
        ApprovedEventFactory.create(tags=["jabolčna čežana", "José", "Django"])
        response = self.client.get(
            reverse('web.search_events'), {
                'q': 'čežana'}, REMOTE_ADDR='93.103.53.11')

        self.assertEquals(1, response.context['events'].count())
        self.assertEquals('SI', response.context['country'])

    def test_search_events_with_search_query_multiple_events(self):
        approved1 = ApprovedEventFactory.create(
            title="Event Arglebargle - Approved", country="SI")
        approved2 = ApprovedEventFactory.create(
            title="Event Arglebargle - Approved", country="AT")

        response = self.client.get(
            reverse('web.search_events'), {
                'q': 'arglebargle'}, REMOTE_ADDR='93.103.53.11')

        self.assertEquals(1, response.context['events'].count())
        self.assertEquals('SI', response.context['country'])

        approved1.delete()
        approved2.delete()

    def test_view_event_without_picture(self):
        test_event = EventFactory.create()
        response = self.client.get(
            reverse(
                'web.view_event',
                args=[
                    test_event.pk,
                    test_event.slug]))

        assert response.status_code == 200
        assert test_event.title in response.content

        test_event.delete()


@pytest.mark.django_db
def test_create_event_with_image(admin_user, admin_client, db):
    with open(local(__file__).dirname + '/../../static/img/team/alja.jpg') as fp:
        io = StringIO.StringIO()
        io.write(fp.read())
        uploaded_picture = InMemoryUploadedFile(
            io, None, "alja.jpg", "jpeg", io.len, None)
        uploaded_picture.seek(0)

    event_data = {
        'audience': [4, 5],
        'theme': [1, 2],
        'contact_person': u'test@example.com',
        'country': u'SI',
        'description': u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\r\ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\r\nquis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\r\nconsequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\r\ncillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\r\nproident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'event_url': u'',
        'location': u'Ljubljana, Slovenia',
        'organizer': u'Mozilla Slovenija',
        'picture': uploaded_picture,
        'start_date': datetime.datetime.now(),
        'end_date': datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
        'tags': [u'css', u'html', u'web'],
        'title': u'Webmaker Ljubljana',
        'user_email': u'test@example.com'
    }

    response = admin_client.post(reverse('web.add_event'), event_data)

    assert response.status_code == 302

    response = admin_client.get(response.url)
    assert 'event_picture/alja' in response.content


@pytest.mark.django_db
def test_edit_event_with_image(admin_user, admin_client, db):
    # First create event
    with open(local(__file__).dirname + '/../../static/img/team/alja.jpg') as fp:
        io = StringIO.StringIO()
        io.write(fp.read())
        uploaded_picture = InMemoryUploadedFile(
            io, None, "alja17.jpg", "jpeg", io.len, None)
        uploaded_picture.seek(0)

    event_data = {
        'audience': [4, 5],
        'theme': [1, 2],
        'contact_person': u'test@example.com',
        'country': u'SI',
        'description': u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\r\ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\r\nquis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\r\nconsequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\r\ncillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\r\nproident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'event_url': u'',
        'location': u'Ljubljana, Slovenia',
        'organizer': u'Mozilla Slovenija',
        'picture': uploaded_picture,
        'start_date': datetime.datetime.now(),
        'end_date': datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
        'tags': [u'css', u'html', u'web'],
        'title': u'Webmaker Ljubljana',
        'user_email': u'test@example.com'
    }

    response = admin_client.post(reverse('web.add_event'), event_data)

    assert response.status_code == 302

    response = admin_client.get(response.url)
    assert 'event_picture/alja' in response.content

    event = Event.objects.latest('id')

    # Then edit it
    with open(local(__file__).dirname + '/../../static/img/team/ercchy.jpg') as fp:
        io = StringIO.StringIO()
        io.write(fp.read())
        uploaded_picture = InMemoryUploadedFile(
            io, None, "ercchy.jpg", "jpeg", io.len, None)
        uploaded_picture.seek(0)

    event_data = {
        'audience': [6, 7],
        'theme': [3, 4],
        'contact_person': u'another_person@example.com',
        'country': u'SI',
        'description': u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\r\ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\r\nquis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\r\nconsequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\r\ncillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\r\nproident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'event_url': u'',
        'location': u'Ljubljana, Slovenia',
        'organizer': u'Mozilla Slovenija',
        'picture': uploaded_picture,
        'start_date': datetime.datetime.now(),
        'end_date': datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
        'tags': [u'css', u'html', u'web'],
        'title': u'Webmaker Ljubljana',
        'user_email': u'another_person@example.com'
    }

    response_edited = admin_client.post(
        reverse(
            'web.edit_event',
            args=[
                event.id]),
        event_data)
    assert response_edited.status_code == 302

    response = admin_client.get(event.get_absolute_url())
    assert 'event_picture/alja17' not in response.content
    assert 'event_picture/ercchy' in response.content

    # Check if the old event picture has been deleted
    old_picture = os.path.isfile(
        local(__file__).dirname +
        '/../../media/event_picture/alja17.jpg')

    assert not old_picture

    event_data = {
        'audience': [6, 7],
        'theme': [3, 4],
        'contact_person': u'another_person@example.com',
        'country': u'SI',
        'description': u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\r\ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\r\nquis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\r\nconsequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\r\ncillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\r\nproident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'event_url': u'',
        'location': u'Ljubljana, Slovenia',
        'organizer': u'Mozilla Slovenija',
        'picture': '',
        'start_date': datetime.datetime.now(),
        'end_date': datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
        'tags': [u'css', u'html', u'web'],
        'title': u'Webmaker Ljubljana',
        'user_email': u'another_person@example.com'
    }

    response_edited = admin_client.post(
        reverse(
            'web.edit_event',
            args=[
                event.id]),
        event_data)
    assert response_edited.status_code == 302

    response = admin_client.get(event.get_absolute_url())
    assert 'event_picture/ercchy' not in response.content


@pytest.mark.django_db
def test_edit_event_without_end_date(db, admin_user, admin_client):
    event = EventFactory.create(creator=admin_user)

    event_data = {
        'audience': [6, 7],
        'theme': [3, 4],
        'contact_person': u'another_person@example.com',
        'country': u'SI',
        'description': u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\r\ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\r\nquis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\r\nconsequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\r\ncillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\r\nproident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'event_url': u'',
        'location': u'Ljubljana, Slovenia',
        'organizer': u'Mozilla Slovenija',
        'picture': '',
        'start_date': datetime.datetime.now(),
        'end_date': '',
        'tags': [u'css', u'html', u'web'],
        'title': u'Webmaker Ljubljana',
        'user_email': u'another_person@example.com'
    }

    response_edited = admin_client.post(
        reverse(
            'web.edit_event',
            args=[
                event.id]),
        event_data)

    assert response_edited.status_code == 200
    assert 'end_date' in response_edited.context['form'].errors

    event.delete()


@pytest.mark.django_db
def test_scoreboard_links_and_results(admin_user, db, client):

    test_country_name = "Slovenia"
    test_country_code = "SI"

    search_url = (reverse('web.search_events') +
                  "?country_code=%s&amp;past=yes" % test_country_code)

    event_data = {
        'audience': [3],
        'theme': [1, 2],
        'country': test_country_code,
        'description': u'Lorem ipsum dolor sit amet.',
        'location': test_country_name,
        'organizer': u'testko',
        "creator": admin_user,
        'start_date': datetime.datetime.now(),
        'end_date': datetime.datetime.now() + datetime.timedelta(days=3, hours=3),
        'title': u'Test Approved Event',
        'status': "APPROVED",
    }

    test_approved_event = create_or_update_event(event_id=None, **event_data)

    for country in count_approved_events_for_country():
        if country['country_code'] == test_country_code:
            event_count = country['events']

    response = client.get(reverse('web.scoreboard'))

    # We're expecting to see this bit of HTML code with the right
    # search URL and the right count for events
    expected_result = '''
	<span class="country-name">%s</span><p> is participating with </p>
	<a href="%s">
	<span class="event-number">%s event
	''' % (test_country_name, search_url, event_count)

    expected_result = expected_result.replace('\t', '').replace('\n', '')
    scoreboard_content = response.content.replace('\t', '').replace('\n', '')

    # The search URL shown on scoreboard also has to match search results
    search_response = client.get(search_url)
    expected_search_result = '<div class="search-counter">%s event' % event_count

    assert expected_result in scoreboard_content
    assert expected_search_result in search_response.content

    test_approved_event.delete()


@pytest.mark.django_db
def test_ambassadors_list(db, client):
    test_country_name = "Austria"
    test_country_code = "AT"

    test_username = 'test-amb'
    test_email = 'test@example.com'
    test_first_name = 'Testko'
    test_last_name = 'Test'
    test_full_name = test_first_name + " " + test_last_name

    test_ambassador = User.objects.create(username=test_username,
                                          email=test_email,
                                          first_name=test_first_name,
                                          last_name=test_last_name)
    test_ambassador_profile = UserProfile.objects.create(
        user=test_ambassador, country=test_country_code)

    group = Group.objects.get(name="ambassadors")
    group.user_set.add(test_ambassador)

    with open(local(__file__).dirname + '/../../static/img/team/alja.jpg') as fp:
        io = StringIO.StringIO()
        io.write(fp.read())
        uploaded_picture = InMemoryUploadedFile(
            io, None, "alja17.jpg", "jpeg", io.len, None)
        uploaded_picture.seek(0)

    avatar = Avatar(user=test_ambassador, primary=True)
    avatar.avatar.save(uploaded_picture.name, uploaded_picture)
    avatar.save()

    new_avatar = get_primary_avatar(test_ambassador, size=80)
    test_amb_avatar = new_avatar.avatar_url(80)

    response = client.get(reverse('web.ambassadors'))

    # We're expecting to the Ambassador under the right country,
    # with the right avatar and the right email contact
    expected_result = '''
	<h2 class="clearfix">%s</h2>
	<div class="ambassador clearfix">
	<img src="%s" alt="%s" width="80" height="80" class="img-circle" />
	<h4>%s&nbsp;<span>&nbsp;<a alt="Send me an email" href="mailto:%s"><i class="fa fa-envelope"></i></a>
	''' % (test_country_name, test_amb_avatar, test_username, test_full_name, test_email)

    expected_result = expected_result.replace('\t', '').replace('\n', '')
    ambassadors_content = response.content.replace('\t', '').replace('\n', '')

# Check this test and modify it to integrating the Ambassadors page changes
    # assert expected_result in ambassadors_content

    test_ambassador.delete()
    avatar.delete()


@pytest.mark.django_db
def test_nonexistent_event(db, client):
    response = client.get(
        reverse(
            'web.view_event',
            args=[
                1234,
                'shouldnt-exist']))

    assert response.status_code == 404


@pytest.mark.django_db
def test_geoip_slovenian_ip(db, client):
    response = client.get('/', REMOTE_ADDR='93.103.53.1')

    assert 'List all events in <span id="country"> Slovenia' in response.content


@pytest.mark.django_db
def test_geoip_invalid_ip(db, client):
    response = client.get('/', REMOTE_ADDR='127.0.0.1')

    assert 'List all events' in response.content
    assert 'List all events <span' not in response.content


@pytest.mark.django_db
def test_list_events_for_country_code(db, client):
    response = client.get(reverse('web.view_event_by_country', args=['SI']))

    assert response.status_code == 200
