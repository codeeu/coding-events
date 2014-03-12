from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from web.processors.event import get_event
from web.processors.user import get_user_profile
from api.models import UserProfile

def can_edit_event(func):
    def decorator(request,*args,**kwargs):
        event = get_event(kwargs['event_id'])
        user = get_user_profile(request.user.id)
        if user.is_ambassador():
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect(reverse('web.index'))
    return decorator




