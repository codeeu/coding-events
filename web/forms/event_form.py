# -*- coding: utf-8 -*-
from django import forms
from django_countries.fields import countries
from api.models import Event
from api.models.events import EventTheme, EventAudience


class AddEventForm(forms.ModelForm):

    email_errors = {
        'required': u'Please enter a valid email, so we can contact you in case of questions.',
        'invalid': u'Can you please check if this is a valid email address?',
    }
    user_email = forms.EmailField(
        required=True,
        label='Your contact email',
        widget=forms.EmailInput(
            attrs={
                "class": "form-control"}),
        error_messages=email_errors,
    )

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
                  'tags',
                  'user_email',
                  ]

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

        if start_date and end_date and end_date < start_date:
            msg = u'End date should be greater than start date.'
            self._errors['end_date'] = self.error_class([msg])

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(AddEventForm, self).__init__(*args, **kwargs)


class ReportEventForm(forms.ModelForm):
    error_css_class = 'has-error'
    required_css_class = 'required'

    class Meta:
        model = Event
        fields = ['participants_count',
                  'average_participant_age',
                  'percentage_of_females',
                  'codeweek_for_all_participation_code',
                  'name_for_certificate',
                  ]

        help_texts = {
            'codeweek_for_all_participation_code': "Optional. You can put here your Codeweek4All challenge code, if you got one. If you're not participating, just ignore this field.",
            'percentage_of_females': "Required. Please provide a rough estimate, even if you don't have exact data. A number from 0 to 100.",
            'average_participant_age': "Required. Please provide a rough estimate, even if you don't have exact data. A number greater than 0.",
            'participants_count': "Required. Please provide a rough estimate, even if you don't have exact data. A number greater than 0.",
            'name_for_certificate': "Required. Change this to the name of the event organizer who will be issued a certificate of participation in Code Week.",
        }

    def __init__(self, *args, **kwargs):
        super(ReportEventForm, self).__init__(*args, **kwargs)

        # Mark all fields as required by default
        for field_name in self.fields:
            self.fields[field_name].required = True

        # Optional fields
        self.fields['codeweek_for_all_participation_code'].required = False


class SearchEventForm(forms.Form):

    countries._countries.append(Event.CUSTOM_COUNTRY_ENTRIES[0])
    countries._countries.append(Event.CUSTOM_COUNTRY_ENTRIES[1])

    # XK is temp code for Kosovo; remove from COUNTRIES_OVERRIDE when
    # Kosovo gets its own ISO code and is added to django-countries
    if not 'Kosovo' in list(dict(countries._countries).values()):
        countries._countries.append((u'XK', u'Kosovo'))

    q = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search for event name or tag',
                'class': 'form-control'}))
    past = forms.ChoiceField(
        label='Include past events',
        required=False,
        choices=(('yes', 'yes'), ('no', 'no')),
        widget=forms.RadioSelect(attrs={'class': 'search-form-element'}),
    )
    country = forms.ChoiceField(
        label='Select country',
        required=False,
        widget=forms.Select(attrs={'class': 'search-form-element'}),
        choices=countries
    )
    theme = forms.ModelMultipleChoiceField(
        queryset=EventTheme.objects.all(),
        label='Theme',
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'search-form-element'}),
    )

    audience = forms.ModelMultipleChoiceField(
        queryset=EventAudience.objects.all(),
        label='Audience',
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'search-form-element'}),
    )

    def __init__(self, *args, **kwargs):
        country_code = kwargs.pop('country_code', None)
        past_events = kwargs.pop('past_events')
        search_query = kwargs.pop('search', None)
        theme = kwargs.pop('theme', None)
        audience = kwargs.pop('audience', None)
        super(SearchEventForm, self).__init__(*args, **kwargs)
        if country_code:
            self.fields['country'].initial = country_code
        self.fields['past'].initial = past_events
        if search_query:
            self.fields['q'].initial = search_query
        if theme:
            self.fields['theme'].initial = theme
        if audience:
            self.fields['audience'].initial = audience
