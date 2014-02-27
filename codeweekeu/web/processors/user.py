from django.contrib.auth.models import User

def get_ambassadors():
	ambassadors = []
	aambassadors = User.objects.filter(groups__name='ambassadors')
	for ambassador in aambassadors:
		ambassadors.append(ambassador.profile)
	return ambassadors
