#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.template import loader, Context
from web.processors.user import get_ambassadors_for_country


'''
Generates and sends event report to ambassadors users
'''


def send_event_report_email(user, event):
    template = loader.get_template("mailer/event_email.txt")
    context = Context({'user': user, 'event': event})

    txt_content = template.render(context)

    send_mail('A new event on codeweek.eu needs your attention',
              txt_content, "info@codeweek.eu", [user.email])


def send_email_to_country_ambassadors(event):
    ambassadors = get_ambassadors_for_country(event.country)
    for user in ambassadors:
        send_event_report_email(user, event)
