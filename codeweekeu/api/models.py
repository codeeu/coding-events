from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
import datetime

class CountryList(models.Model):
	name = models.CharField(max_length=255)

	def __unicode__(self):
		return '{0}'.format(self.name)

class Event(models.Model):

	PENDING_STATUS=1
	APPROVED_STATUS=2

	STATUS_CHOICES=(
		(APPROVED_STATUS, 'APPROVED'),
		(PENDING_STATUS, 'PENDING'),
	)

	status=models.IntegerField(choices=STATUS_CHOICES,default=1)
	title=models.CharField(max_length=255)
	organizer=models.CharField(max_length=255)
	description=models.TextField(max_length=1000)
	location=models.CharField(max_length=1000)
	country=models.ForeignKey(CountryList)
	start_date=models.DateTimeField()
	end_date=models.DateTimeField()
	event_url=models.URLField(blank=True)
	contact_person=models.EmailField(blank=True)
	#tags=TaggableManager()
	picture= models.ImageField(upload_to='event_avatars',default='http://placehold.it/400',blank=True)
	pub_date=models.DateTimeField(default=datetime.datetime.now())


	def __unicode__(self):
		return self.title


	class Meta:
		ordering=['start_date']


class SocialAccountList(models.Model):
	name=models.CharField(max_length=255)
	owner=models.ForeignKey(User)

	def __unicode__(self):
		return '{0}'.format(self.name)



class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	country=models.ForeignKey(CountryList)
	social_account_list=models.ForeignKey(SocialAccountList)

	def __unicode__(self):
		return '%s' % self.user.email

