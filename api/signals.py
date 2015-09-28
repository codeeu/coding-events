from django.contrib import messages
from django.contrib.auth.signals import user_logged_in
from django.template import loader, Context
from api.processors import get_pending_events


def check_pending_events(sender, user, request, **kwargs):
    if user.profile.is_ambassador():

        if not user.profile.country:
            t = loader.get_template('alerts/set_country_request.html')
            c = Context({'user': user, })
            messages.warning(request, t.render(c))
        else:

            args = {}

            if not request.user.is_staff:
                args['country_code'] = user.profile.country.code

            pending_events = get_pending_events(**args)

            if pending_events:
                t = loader.get_template('alerts/pending_events.html')
                c = Context({'user': user, })
                messages.warning(request, t.render(c))
    else:
        return None


user_logged_in.connect(check_pending_events)
