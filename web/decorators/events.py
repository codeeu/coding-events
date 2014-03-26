from functools import wraps
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import login

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from api.processors import get_event_by_id
from web.processors.user import get_user_profile


def can_edit_event(func):
	def decorator(request, *args, **kwargs):
		event = get_event_by_id(kwargs['event_id'])
		if request.user.id == event.creator.id:
			return func(request, *args, **kwargs)
		else:
			return HttpResponseRedirect(reverse('web.index'))

	return decorator

def can_moderate_event(func):
	def decorator(request, *args, **kwargs):
		event = get_event_by_id(kwargs['event_id'])
		user = get_user_profile(request.user.id)
		if user.is_ambassador():
			return func(request, *args, **kwargs)
		else:
			return HttpResponseRedirect(reverse('web.index'))

	return decorator

def login_required_ajax(function=None, redirect_field_name=None):
	"""
	Just make sure the user is authenticated to access a certain ajax view

	Otherwise return a HttpResponse 401 - authentication required
	instead of the 302 redirect of the original Django decorator
	"""

	def _decorator(view_func):
		def _wrapped_view(request, *args, **kwargs):
			if request.user.is_authenticated():
				return view_func(request, *args, **kwargs)
			else:
				print 'open modal'
			#return HttpResponse(status=401)

		return _wrapped_view

	if function:
		return _decorator(function)
	return _decorator


def login_required(view_callable):
	def check_login(request, *args, **kwargs):
		if request.user.is_authenticated():
			return view_callable(request, *args, **kwargs)

		assert hasattr(request, 'session'), 'Session middleware needed.'
		login_kwargs = {
			'extra_context': {
				REDIRECT_FIELD_NAME: request.get_full_path(),
				'modal': True,
			},
		}

		#return login(request, template_name='pages/add_event.html', **login_kwargs)
		request.session['modal'] = True
		return HttpResponseRedirect(reverse('web.index'))

	return wraps(view_callable)(check_login)




