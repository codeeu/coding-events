from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from web.forms.user_profile import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required


@login_required()
def user_profile(request):

	if request.method == 'POST':
		# populate form with original instance and add post info on top of that
		uform = UserForm(request.POST, instance=request.user)
		pform = UserProfileForm(request.POST, instance=request.user.profile)
		if uform.is_valid() and pform.is_valid():
			uform.save()
			pform.save()
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