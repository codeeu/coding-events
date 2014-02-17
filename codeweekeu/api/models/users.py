from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class UserProfile(models.Model):
	"""
	Extending User Model
	"""
	user = models.OneToOneField(User)
	country = CountryField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return 'Username: %s, First Name:%s Last Name: %s, Country: %s' % \
			(self.user.username, self.user.first_name, self.user.last_name, self.country)

	class Meta:
		app_label = 'api'

# It forces to get or create profile when User is accessed
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class SocialAccountList(models.Model):
	name = models.CharField(max_length=255)
	owner = models.ForeignKey(User)

	def __unicode__(self):
		return '{0}'.format(self.name)

	class Meta:
		app_label = 'api'

