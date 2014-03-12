from calendar import HTMLCalendar
from django import template
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc

register = template.Library()


class EventCalendar(HTMLCalendar):
	"""
	Overload Python's calendar.HTMLCalendar to add the appropriate events to
	each day's table cell.
	"""

	def __init__(self, start_day, end_day):
		super(EventCalendar, self).__init__()
		self.start_day = start_day.date().day
		self.end_day = end_day.date().day

	def formatday(self, day, weekday):
		if day != 0:
			cssclass = self.cssclasses[weekday]
			if date.today() == date(self.year, self.month, day):
				cssclass += ' today'
			if self.start_day <= day <= self.end_day:
				cssclass += ' filled'
				body = []
				return self.day_cell(cssclass, '<span class="dayNumber">%d</span> %s' % (day, ''.join(body)))
			return self.day_cell(cssclass, '<span class="dayNumberNoEvents">%d</span>' % (day))
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

	return mark_safe(cal.formatmonth(2014, 3))
