from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib import messages

from web.forms.user_profile import UserForm, UserProfileForm
from web.views.events import get_client_ip

from web.processors.user import get_ambassadors_for_countries
from web.processors.event import get_country_from_user_ip
from web.decorators.events import login_required


def login(request):

	next_path = request.GET.get('next', None)

	return render_to_response('pages/login.html', {
		'next': next_path

	}, context_instance=RequestContext(request))

@login_required
def user_profile(request):
	if request.method == 'POST':
		# populate form with original instance and add post info on top of that
		uform = UserForm(request.POST, instance=request.user)
		pform = UserProfileForm(request.POST, instance=request.user.profile)
		if uform.is_valid() and pform.is_valid():
			uform.save()
			pform.save()
			messages.success(request, 'Profile details updated')
	else:
		user = request.user
		uform = UserForm(instance=user)
		profile = user.profile
		pform = UserProfileForm(instance=profile)

	context = {}
	context.update(csrf(request))
	context['uform'] = uform
	context['pform'] = pform

	return render_to_response(
		'pages/profile.html', context, context_instance=RequestContext(request))


def ambassadors(request):
	try:
		user_ip = get_client_ip(request)
		user_country = get_country_from_user_ip(user_ip)
	except:
		user_country = None

	countries_ambassadors = get_ambassadors_for_countries()

	return render_to_response(
		'pages/ambassadors.html', {
		'user_country': user_country,
		'countries': countries_ambassadors,
		},
		context_instance=RequestContext(request))

