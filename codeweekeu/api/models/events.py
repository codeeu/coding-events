import datetime
from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django_countries.fields import CountryField
from geoposition.fields import GeopositionField

class Event(models.Model):

	def __init__(self,*args,**kwargs):

		try:
			self.tag=kwargs["tags"]
			del kwargs["tags"]
		except KeyError:
			pass

		super(Event,self).__init__(*args,**kwargs)


	STATUS_CHOICES = (
		(1, 'Approved'),
		(2, 'Pending'),
	)
	status = models.IntegerField(choices=STATUS_CHOICES, default=1)
	title = models.CharField(max_length=255)
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

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['start_date']
		app_label = 'api'


	def save(self,*args,**kwargs):
		super(Event,self).save(*args,**kwargs)

		try:
			for tag in self.tag:
				self.tags.add(tag)
		except AttributeError:
			pass





