"""
Models for the event
"""
import datetime
from django.utils import timezone
from django.db import models
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
from geoposition.fields import GeopositionField
from django_countries.fields import CountryField
from django.conf import settings
from django.contrib.auth.models import User

class EventAudience(models.Model):
	name = models.CharField(max_length=255) 

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'api'


class EventTheme(models.Model):
	name = models.CharField(max_length=255) 

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'api'


class Event(models.Model):

	STATUS_CHOICES = (
		('APPROVED', 'Approved'),
		('PENDING', 'Pending'),
	    ('REJECTED', 'Rejected'),
	)
	status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')
	title = models.CharField(max_length=255, default=None)
	slug = models.SlugField(max_length=255, null=True, blank=True)
	creator = models.ForeignKey(User)
	organizer = models.CharField(max_length=255, default=None)
	description = models.TextField(max_length=1000)
	geoposition = GeopositionField()
	location = models.CharField(max_length=1000)
	country = CountryField()
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	event_url = models.URLField(blank=True)
	contact_person = models.EmailField(blank=True)
	picture = models.ImageField(upload_to=settings.MEDIA_UPLOAD_FOLDER, blank=True)
	pub_date = models.DateTimeField(default=datetime.datetime.now())
	audience = models.ManyToManyField(EventAudience, related_name='event_audience')
	theme = models.ManyToManyField(EventTheme, related_name='event_theme')
	tags = TaggableManager(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['start_date']
		app_label = 'api'
		permissions = (
			('edit_event', 'Can edit event'),
			('submit_event', 'Can submit event'),
			('reject_event', 'Can reject event'),
		)

	def __init__(self, *args, **kwargs):
		try:
			self.tag = kwargs['tags']
			del kwargs['tags']
		except KeyError:
			pass

		try:
			self.audiencelist = kwargs['audience']
			del kwargs['audience']
		except KeyError:
			pass

		try:
			self.themelist = kwargs['theme']
			del kwargs['theme']
		except KeyError:
			pass

		super(Event, self).__init__(*args, **kwargs)

	def save(self, *args, **kwargs):		
		if not self.id:
			self.slug = slugify(self.title)
		super(Event, self).save(*args, **kwargs)

		try:
			for tag in self.tag:
				self.tags.add(tag)
			for entry in self.audiencelist:
				self.audience.add(entry)
			for entry in self.themelist:
				self.theme.add(entry)
		except AttributeError:
			pass

	def get_tags(self):
		return ', '.join([e.name for e in self.tags.all()])

	def get_audience_array(self):
		return [audience.pk for audience in self.audience.all()]

	def get_theme_array(self):
		return [theme.pk for theme in self.theme.all()]

	def has_started(self):
		return timezone.now() > self.start_date

	def has_ended(self):
		return timezone.now() > self.end_date


