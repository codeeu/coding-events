from django.contrib.auth.models import User
from django_countries import countries

def get_user(user_id):
    user = User.objects.get(id=user_id)
    return user

def get_user_profile(user_id):
    user = User.objects.get(id=user_id)
    return user.profile

def get_ambassadors(country_code=None):
	ambassadors = []
	all_ambassadors = User.objects.filter(groups__name='ambassadors').order_by('date_joined')
	for ambassador in all_ambassadors:
		if country_code:
			if ambassador.profile.country == country_code:
				ambassadors.append(ambassador.profile)
		else:
			ambassadors.append(ambassador.profile)
	return ambassadors

def get_main_ambassadors(country_code=None):
	ambassadors = []
	all_ambassadors = User.objects.filter(groups__name='main').order_by('date_joined')
	for ambassador in all_ambassadors:
		if country_code:
			if ambassador.profile.country == country_code:
				ambassadors.append(ambassador.profile)
		else:
			ambassadors.append(ambassador.profile)
	return ambassadors

def get_not_main_ambassadors(country_code=None):
	ambassadors = []
	all_ambassadors = User.objects.filter(groups__name='ambassadors').exclude(groups__name='main').order_by('date_joined')
	for ambassador in all_ambassadors:
		if country_code:
			if ambassador.profile.country == country_code:
				ambassadors.append(ambassador.profile)
		else:
			ambassadors.append(ambassador.profile)
	return ambassadors

def get_ambassadors_for_countries():
	ambassadors = get_ambassadors()
	countries_ambassadors = []
	# list countries minus two CUSTOM_COUNTRY_ENTRIES
	for code, name in list(countries)[2:]:
		readable_name = unicode(name)
		main_ambassadors = get_main_ambassadors(code)
		found_ambassadors = get_not_main_ambassadors(code)
		countries_ambassadors.append((code, readable_name,found_ambassadors, main_ambassadors))

	countries_ambassadors.sort()
	return countries_ambassadors

def get_ambassadors_for_country(country):
	ambassadors = User.objects.filter(groups__name='ambassadors', userprofile__country=country)
	return ambassadors


def update_user_email(user_id, new_email):
	user = User.objects.get(id=user_id)
	user.email = new_email
	user.save(update_fields=["email"]) 
	return user
