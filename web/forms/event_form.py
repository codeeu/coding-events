# -*- coding: utf-8 -*-
from django import forms
from django_countries.fields import countries
from api.models import Event
from api.models.events import EventTheme, EventAudience


class AddEventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['title', 'organizer', 'description', 'geoposition', 'location', 'country', 'start_date', 'end_date',
				  'event_url', 'contact_person', 'audience', 'theme', 'picture', 'tags']

		widgets = {
			'title': forms.TextInput(attrs={"class": "form-control"}),
			'organizer': forms.TextInput(attrs={"class": "form-control"}),
			'description': forms.Textarea(attrs={"class": "form-control"}),
			'location': forms.TextInput(attrs={"id": "autocomplete", "placeholder": "Search for your address",
											   "class": "form-control"}),
			'start_date': forms.TextInput(attrs={"id": "id_datepicker_start", "class": "form-control",}),
			'end_date': forms.TextInput(attrs={"id": "id_datepicker_end", "class": "form-control"}),
			'event_url': forms.TextInput(attrs={"class": "form-control"}),
			'contact_person': forms.TextInput(attrs={"class": "form-control"}),
			'audience': forms.CheckboxSelectMultiple(),
			'theme': forms.CheckboxSelectMultiple(),
			'tags': forms.TextInput(attrs={"class": "form-control"}),
		}

		labels = {
			'title': 'Your event\'s title:',
			'organizer': 'Who\'s organizing this event?',
			'description': 'Short event description:',
			'location': 'Where will the event be taking place?',
			'country': 'Event\'s country:',
			'start_date': 'When does the event start?',
			'end_date': 'When does the event end?',
			'event_url': 'Do you have a website with more information about the event?',
			'contact_person': 'Would you like to display a contact email?',
			'picture': 'You can also upload an image to represent your event:',
			'audience': 'Who is the event for?',
			'theme': 'Which aspect of coding will your event cover?',
			'tags': 'Tags, separated by commas:',
		}
		error_messages = {
			'title': {
				'required': u'Please enter a title for your event.',
				'invalid': u'Can you please check if this is a valid title?',
			},
			'organizer': {
				'required': u'Please enter an organizer.',
				'invalid': u'Can you please check if this is a valid organizer?',
			},
			'description': {
				'required': u'Please write a short description of what the event is about.',
				'invalid': u'Please check if the description only contains regular text.',
			},
			'geoposition': {
				'invalid': u'Please enter valid coordinates.'
			},
			'location': {
				'required': u'Please enter a location or use online for web-based events.',
				'invalid': u'Please check your event\'s location',
			},
			'country': {
				'required': u'The event\'s location should be in Europe.',
				'invalid': u'Make sure the event country is written in English.',
			},
			'start_date': {
				'required': u'Please enter a valid date and time (example: 2014-10-22 18:00).',
				'invalid': u'This doesn\'t seem like a valid date and time. Can you check, please?',
			},
			'end_date': {
				'required': u'Please enter a valid date and time (example: 2014-10-22 20:00).',
				'invalid': u'This doesn\'t seem like a valid date and time. Can you check, please?',
			},
			'event_url': {
				'invalid': u'Please enter a valid web address starting with http://',
			},
			'contact_person': {
				'invalid': u'Please enter a valid email address.',
			},
			'picture': {
				'invalid': u'Make sure this is a valid image.',
			},
			'audience': {
				'required': u'If unsure, choose Other and provide more information in the description.',
				'invalid': u'Choose one or more of the provided choices.',
			},
			'theme': {
				'required': u'If unsure, choose Other and provide more information in the description.',
				'invalid': u'Choose one or more of the provided choices.',
			},
			'tags': {
				'required': u'Please type in some tags to categorize the event',
				'invalid': u'Please enter tags in plain text, separated by commas.',
			},
		}

	def __init__(self, *args, **kwargs):
		super(AddEventForm, self).__init__(*args, **kwargs)


class SearchEventForm(forms.Form):

	search = forms.CharField(
		required=False,
		widget=forms.TextInput(attrs={'placeholder': 'Search some serious events', 'class': 'form-control'})
	)
	country = forms.ChoiceField(
		label='Select country',
		required=False,
		widget=forms.Select(attrs={'class': 'form-control search-form-element'}),
		choices=countries
	)
	theme = forms.ModelMultipleChoiceField(
		queryset=EventTheme.objects.all(),
		label='Theme',
		required=False,
		widget=forms.CheckboxSelectMultiple(attrs={'class': 'search-form-element'}),
	)

	audience = forms.ModelMultipleChoiceField(
		queryset=EventAudience.objects.all(),
		label='Audience',
		required=False,
		widget=forms.CheckboxSelectMultiple(attrs={'class': 'search-form-element'}),
	)

	def __init__(self, *args, **kwargs):
		country_code = kwargs.pop('country_code', None)
		super(SearchEventForm, self).__init__(*args, **kwargs)
		if country_code:
			self.fields['country'].initial = country_code





