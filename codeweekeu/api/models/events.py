import datetime
from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django_countries.fields import CountryField
from api.managers.event_managers import EventSelectorManager
from geoposition.fields import GeopositionField
from django.template.defaultfilters import slugify

class Event(models.Model):

	def __init__(self,*args,**kwargs):

		try:
			self.tag=kwargs["tags"]
			del kwargs["tags"]
		except KeyError:
			pass

		super(Event,self).__init__(*args,**kwargs)

	APPROVED=2
	PENDING=1

	STATUS_CHOICES = (
		(APPROVED, 'Approved'),
		(PENDING, 'Pending'),
	)
	status = models.IntegerField(choices=STATUS_CHOICES, default=1)
	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, null=True, blank=True)
	organizer = models.CharField(max_length=255)
	description = models.TextField(max_length=1000)
	geoposition = GeopositionField()
	location = models.CharField(max_length=1000)
	country = CountryField()
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	event_url = models.URLField(blank=True)
	contact_person = models.EmailField(blank=True)
	picture = models.ImageField(upload_to='event_picture', blank=True)
	pub_date = models.DateTimeField(default=datetime.datetime.now())
	tags=TaggableManager()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)

	approved=EventSelectorManager(status=APPROVED)
	pending=EventSelectorManager(status=PENDING)
	objects = models.Manager()

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['start_date']
		app_label = 'api'
		permissions= (
			("edit_event","Can edit event"),
			("submit_event", "Can submit event"),
			("reject_event", "Can reject event"),
		)
	def save(self,*args,**kwargs):
		if not self.id:
			self.slug = slugify(self.title)
		super(Event,self).save(*args,**kwargs)

		try:
			for tag in self.tag:
				self.tags.add(tag)
		except AttributeError:
			pass


