"""
Django settings for codeweekeu project.
"""

import os

here = lambda x: os.path.join(os.path.dirname(os.path.abspath(__file__)), x)
PROJECT_DIR = here

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': here('../codeweekeu.db'),
		# The following settings are not used with sqlite3:
		'USER': '',
		'PASSWORD': '',
		'HOST': '',
		'PORT': '',
	}
}

ALLOWED_HOSTS = []
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd7o9p97d9d6t&ycz^aennig5!65xv8g!ba!#cezu(*^&h0bv8!'

MEDIA_ROOT = here('../media/')
MEDIA_URL = '/media/'

STATIC_ROOT = here('../staticfiles/')
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
	here('../static/'),
)

LOGIN_REDIRECT_URL = '/'

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'codeweekeu.urls'

WSGI_APPLICATION = 'codeweekeu.wsgi.application'

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'debug_toolbar.middleware.DebugToolbarMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.request',
	'django.core.context_processors.media',
	'social.apps.django_app.context_processors.backends',
	'social.apps.django_app.context_processors.login_redirect',
)

TEMPLATE_DIRS = (
	here('../web/templates'),
)

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.admindocs',
	'debug_toolbar',
	'social.apps.django_app.default',
	'django_countries',
	'avatar',
	'web',
	'api',
	'taggit',
)

AUTH_PROFILE_MODULE = 'api.UserProfile'

AUTHENTICATION_BACKENDS = (
	'social.backends.github.GithubOAuth2',
	'social.backends.twitter.TwitterOAuth',
	'social.backends.facebook.FacebookOAuth2',
	'social.backends.facebook.FacebookAppOAuth2',
	'social.backends.google.GoogleOpenId',
	'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GITHUB_KEY = ''
SOCIAL_AUTH_GITHUB_SECRET = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '...'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '...'
SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_TWITTER_KEY = ''
SOCIAL_AUTH_TWITTER_SECRET = ''

SOCIAL_AUTH_ENABLED_BACKENDS = ('github', 'twitter', 'facebook', 'google')
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/login-error/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/accounts/profile/'

#############################################################################
# Django debug toolbar settings
#############################################################################
INTERNAL_IPS = ('127.0.0.1',)

#############################################################################
# Logging settings
#############################################################################
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler'
		}
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True,
		},
	}
}

try:
	from settings_local import *
except ImportError, e:
	pass
