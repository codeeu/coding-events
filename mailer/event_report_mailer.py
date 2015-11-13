#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.template import loader, Context
from django.conf import settings
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


def send_reminder_for_event_report_and_certificate(
        user,
        unreported_events_count,
        previous_emails_count=0,
        max_emails_count=None,
        test_mode=False
    ):
    template = loader.get_template("mailer/reminder_for_event_report_and_certificate.txt")
    context = Context({
        'name': user.full_name(),
        'email': user.email,
        'previous_emails_count': previous_emails_count,
        'total_emails_count': previous_emails_count + 1,
        'max_emails_count': max_emails_count,
        'unreported_events_count': unreported_events_count,
    })

    content   = template.render(context)
    subject   = '[CodeWeekEU] your feedback and your certificate of recognition'
    sender    = settings.EVENT_REPORT_REMINDERS_FROM_EMAIL
    recipient = user.email_with_name()

    if test_mode:
        print("------------------------------------------------------------")
        print(u"To: " + recipient)
        print(u"From: " + sender)
        print(u"Subject: " + subject)
        print(u"\n" + content)
        print("------------------------------------------------------------")
    else:
        send_mail(subject, content, sender, [recipient])
