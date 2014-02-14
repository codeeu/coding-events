from django import forms
from api.models import User
from api.models import UserProfile


class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']
		labels = {
			'first_name': 'Your valued name',
			'last_name': 'What your mommy and daddy gave you',
		    'email': 'where you get spam?',
		}


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('country',)
		labels = {'country': 'Country', }
		#labels = {'country': 'Country', }
		help_texts = {'country': 'Tell us what is the place you call home.', }
		error_messages = {
            'country': {
                'max_length': 'Are you sure? Where is that?',
            },
        }