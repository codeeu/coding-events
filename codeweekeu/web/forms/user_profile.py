from django import forms
from api.models.users import User
from api.models.users import UserProfile


class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']
		labels = {
			'first_name': 'Your Valued Name',
			'last_name': 'What name did Your Mommy and Daddy Gave You?',
		    'email': 'Where Do You Get Your Spam?',
		}
		help_text = {
			'first_name': 'Your First Name',
			'last_name': 'Last Name',
		    'email': 'Email',
		}


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('country',)
		labels = {'country': 'Country', }
		help_texts = {'country': 'Tell Us What Is The Name Of The Place You Call Home.', }
		error_messages = {
            'country': {
                'max_length': 'Are you sure? Where is that?',
            },
        }