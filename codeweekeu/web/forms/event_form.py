# -*- coding: utf-8 -*-
from django import forms
from django.utils.html import  escape

class AddEvent(forms.Form):

	title = forms.CharField(
		required=True, 
		max_length=100,
		label='Your event\'s title:', 
		widget=forms.widgets.TextInput(),
		error_messages = {
			'required': u'Please enter a title for your event.',
			'invalid': u'Can you please check if this is a valid title?',
		},
		)

	organizer = forms.CharField(
		required=True, 
		max_length=140,
		label='Who\'s organizing this event?',
		widget=forms.widgets.TextInput(),
		error_messages = {
			'required': u'Please enter an organizer.',
			'invalid': u'Can you please check if this is a valid organizer?',
		},
		)

	description = forms.CharField(
		required=True,
		label='Short event description:',
		widget=forms.widgets.Textarea(),
		error_messages = {
			'required': u'Please write a short description of what the event is about.',
			'invalid': u'Please check if the description only contains regular text.',
		},
		)

	location = forms.CharField(
		required=True,
		label='Where will the event be taking place?',
		widget=forms.widgets.TextInput(),
		error_messages = {
			'required': u'Please enter a location or use online for web-based events.',
			'invalid': u'Please check your event\'s location',
		},
		)

	country = forms.CharField(
		required=True,
		label='Event\'s country:',
		widget=forms.widgets.TextInput(),
		error_messages = {
			'required': u'Please select the event\'s country.',
			'invalid': u'Make sure the event country is written in English.',
		},
		)

	start_date = forms.DateTimeField(
		required=False,
		label='When does the event start?',
		error_messages = {
			'required': u'Please enter a valid date and time.',
			'invalid': u'This doesn\'t seem like a valid date and time. Can you check, please?',
		},
		)

	end_date = forms.DateTimeField(
		required=False,
		label='When does the event end?',
		error_messages = {
			'required': u'Please enter a valid date and time.',
			'invalid': u'This doesn\'t seem like a valid date and time. Can you check, please?',
		},
		)

	event_url = forms.URLField(
		required=False,
		label='Do you have a website with more information about the event? (optional)',
		error_messages = {
			'invalid': u'Please enter a valid web address starting with http://',
		},
		)

	contact_person = forms.EmailField(
		required=False,
		label='Would you like to display a contact email? (optional)',
		error_messages = {
			'invalid': u'Please enter a valid email address.',
		},
		)

	tags = forms.CharField(
		required=True,
		label='Tags for your event:',
		widget=forms.widgets.TextInput(),
		error_messages = {
			'invalid': u'That\'s not a valid tag, please check.',
		},
		)

	picture = forms.ImageField(
		required=False,
		label='You can also upload an image to represent your event: (optional)',
		error_messages = {
			'invalid': u'Make sure this is a valid image.',
		},
		)

	def is_valid(self):
		form = super(AddEvent, self).is_valid()
		for f,error in self.errors.iteritems():
			if f != '__all__':
				error=escape(str(error))
				self.fields[f].widget.attrs.update({'class': 'error',})
		return form
