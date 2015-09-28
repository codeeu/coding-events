import ast

from calendar import HTMLCalendar
from django import template
from datetime import date
from itertools import groupby
from django.core import urlresolvers

from django.utils.html import conditional_escape as esc

register = template.Library()


class EventCalendar(HTMLCalendar):
    """
    Overload Python's calendar.HTMLCalendar to add the appropriate events to
    each day's table cell.
    """

    def __init__(self, start_day, end_day):
        super(EventCalendar, self).__init__()
        self.start_day = start_day.date()
        self.end_day = end_day.date()

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if self.start_day.month != self.end_day.month:
                if self.start_day.day <= day:
                    cssclass += ' filled'
                    body = []
                    return self.day_cell(
                        cssclass, '<span class="dayNumber">%d</span> %s' %
                        (day, ''.join(body)))
            if self.start_day.day <= day <= self.end_day.day:
                cssclass += ' filled'
                body = []
                return self.day_cell(
                    cssclass, '<span class="dayNumber">%d</span> %s' %
                    (day, ''.join(body)))
            return self.day_cell(
                cssclass,
                '<span class="dayNumberNoEvents">%d</span>' %
                (day))
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

    def group_by_day(self, events):
        field = lambda event: event.date_and_time.day
        return dict(
            [(day, list(items)) for day, items in groupby(events, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)


@register.filter('render_calendar')
def render_calendar(event_start_date, event_end_date):
    from django.utils.safestring import mark_safe

    cal = EventCalendar(event_start_date, event_end_date)

    return mark_safe(
        cal.formatmonth(
            event_start_date.year,
            event_start_date.month))


@register.simple_tag(takes_context=True)
def current(context, url_name, return_value=' active', **kwargs):
    matches = current_url_equals(context, url_name, **kwargs)
    return return_value if matches else ''


def current_url_equals(context, url_name, **kwargs):
    resolved = False
    try:
        resolved = urlresolvers.resolve(context.get('request').path)
    except:
        pass
    matches = resolved and resolved.url_name == url_name
    if matches and kwargs:
        for key in kwargs:
            kwarg = kwargs.get(key)
            resolved_kwarg = resolved.kwargs.get(key)
            if not resolved_kwarg or kwarg != resolved_kwarg:
                return False
    return matches


@register.filter('from_current_country')
def events_from_selected_country(event_list, current_country_code):
    for country in event_list:
        if country['grouper'].code == current_country_code:
            return country

    return {'grouper': '', 'list': []}
