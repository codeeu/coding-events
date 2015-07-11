# This should be removed if we upgrade Django and python-social-auth to
# newer versions.
def patch_social_auth_to_enable_searching_in_django_1_6():
	from social.apps.django_app.default.admin import UserSocialAuthOption

	UserSocialAuthOption.search_fields = ['user__email', 'user__username', 'uid']

patch_social_auth_to_enable_searching_in_django_1_6()
