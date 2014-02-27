from django.contrib.auth.models import User
from django_countries import countries

def get_ambassadors():
	ambassadors = []
	aambassadors = User.objects.filter(groups__name='ambassadors')
	for ambassador in aambassadors:
		ambassadors.append(ambassador.profile)
	return ambassadors

def get_ambassadors_for_countries():
	ambassadors = get_ambassadors()
	countries_ambassadors = []
	for code, name in list(countries):
		readable_name = unicode(name)
		found_ambassadors = []
		for ambassador in ambassadors:
			if ambassador.country == code:
				found_ambassadors.append(ambassador)
		countries_ambassadors.append((readable_name,found_ambassadors))
	countries_ambassadors.sort()
	return countries_ambassadors
