# -*- coding: utf-8 -*-
from django import forms
from django_countries.fields import countries
from api.models import Event
from api.models.events import EventTheme, EventAudience


class AddEventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['title',
		          'organizer',
		          'description',
		          'geoposition',
		          'location',
		          'country',
		          'start_date',
		          'end_date',
		          'event_url',
		          'contact_person',
		          'audience',
		          'theme',
		          'picture',
		          'tags']

		widgets = {
			'title': forms.TextInput(attrs={"class": "form-control",
				                       		"placeholder": "How do you call this event?"}),
			'organizer': forms.TextInput(attrs={"class": "form-control",
				                       			"placeholder": "Who is organizing this event?"}),
			'description': forms.Textarea(attrs={"class": "form-control",
			                                     "placeholder": "Tell us a bit about your event."}),
			'location': forms.TextInput(attrs={"id": "autocomplete", "class": "form-control",
			                                   "placeholder": "Where will the event be taking place?", }),
			'start_date': forms.TextInput(attrs={"id": "id_datepicker_start", "class": "form-control",
			                                     "autocomplete": "off",
			                                     "placeholder": "When does it start?"}),
			'end_date': forms.TextInput(attrs={"id": "id_datepicker_end", "class": "form-control",
			                                   "autocomplete": "off", "placeholder": "When does it end?"}),
			'event_url': forms.TextInput(attrs={"class": "form-control",
			                                    "placeholder": "Do you have a website with more information?"}),
			'contact_person': forms.TextInput(attrs={"class": "form-control",
			                                         "placeholder": "Would you like to display a contact email?"}),
			'audience': forms.CheckboxSelectMultiple(),
			'theme': forms.CheckboxSelectMultiple(),
			'tags': forms.TextInput(attrs={"class": "form-control",
			                               "placeholder": "example: Python, Django, Slovenia"}),
		}

		labels = {
			'title': 'Event title',
			'organizer': 'Organizer(s)',
			'description': 'Description',
			'location': 'Location',
			'country': 'Country',
			'start_date': 'Start date',
			'end_date': 'End date',
			'event_url': 'Website',
			'contact_person': 'Contact',
			'picture': 'Image',
			'audience': 'Audience',
			'theme': 'Theme',
			'tags': 'Tags',
		}

		help_texts = {
			'start_date': "Example: YYYY/MM/DD h:m",
		    'end_date': "Example: YYYY/MM/DD h:m",
		    'audience': "Who is the event for?",
		    'theme': "Which aspect of coding will your event cover?",
		    'picture': 'Larger images will be resized to 256 x 512 pixels. Maximum upload size is 256 x 1024.',
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
				'required': u'Please enter a location.',
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

	def clean(self):
		cleaned_data = super(AddEventForm, self).clean()
		start_date = cleaned_data.get('start_date')
		end_date = cleaned_data.get('end_date')

		if end_date < start_date:
			msg = u'End date should be greater than start date.'
			self._errors['end_date'] = self.error_class([msg])

		return cleaned_data

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





