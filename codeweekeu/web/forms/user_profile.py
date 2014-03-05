from django import forms
from api.models.users import User
from api.models.users import UserProfile


class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']
		labels = {
			'first_name': 'Your first name:',
			'last_name': 'Your last name:',
		    'email': 'Your contact email:',
		}
		help_text = {
			'first_name': 'Your First Name',
			'last_name': 'Last Name',
		    'email': 'Email',
		}


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('country', 'bio', 'website', 'twitter')
		labels = {
			'country': 'Your country:',
			'bio': 'Short bio:',
			'website': 'Your website:',
			'twitter': 'Twitter handle: @',
			}
		help_texts = {'country': 'If unsure, select the country in which you\'ll be active during Code Week', }
		error_messages = {
            'country': {
                'max_length': 'Are you sure? Where is that?',
            },
			'website': {
				'invalid': 'Please enter a valid web address',
			},
			}
