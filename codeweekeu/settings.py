"""
Django settings for codeweekeu project.
"""

import sys
import os
from os.path import abspath, basename, dirname, join, normpath
########## PATH CONFIGURATION
# Absolute filesystem path to this Django project directory.
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Site name.
# SITE_NAME = basename(DJANGO_ROOT)
SITE_NAME = 'codeweekeu'


# Absolute filesystem path to the top-level project folder.
SITE_ROOT = dirname(DJANGO_ROOT)


# Absolute filesystem path to the secret file which holds this project's
# SECRET_KEY. Will be auto-generated the first time this file is interpreted.
SECRET_FILE = normpath(join(SITE_ROOT, 'deploy', 'SECRET'))


# Add all necessary filesystem paths to our system path so that we can use
# python import statements.
sys.path.append(SITE_ROOT)
sys.path.append(normpath(join(DJANGO_ROOT, 'api')))
sys.path.append(normpath(join(DJANGO_ROOT, 'web')))
########## END PATH CONFIGURATION

########## DEBUG CONFIGURATION
# Disable debugging by default.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

########## END DEBUG CONFIGURATION

########## MANAGER CONFIGURATION
# Admin and managers for this project. These people receive private site
# alerts.
ADMINS = (
    ('Errors', 'errors@codeweek.eu'),
)

MANAGERS = ADMINS
########## END MANAGER CONFIGURATION

########## DATABASE CONFIGURATION
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': normpath(join(DJANGO_ROOT, 'db', 'default.db')),
		'USER': '',
		'PASSWORD': '',
		'HOST': '',
		'PORT': '',
	}
}
########## END DATABASE CONFIGURATION

ALLOWED_HOSTS = ['localhost', 'codeweek.eu']
########## GENERAL CONFIGURATION
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name although not all
# choices may be available on all operating systems. On Unix systems, a value
# of None will cause Django to use the same timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Ljubljana'


# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html.
LANGUAGE_CODE = 'sl'

USE_TZ = False

# Dummy function, so that "makemessages" can find strings which should be translated.
_ = lambda s: s
LANGUAGES = (
    ('sl', _('Slovenian')),
	('en', _('English')),
)


# The ID, as an integer, of the current site in the django_site database table.
# This is used so that application data can hook into specific site(s) and a
# single database can manage content for multiple sites.
SITE_ID = 1


# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_L10N = True


# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True
########## END GENERAL CONFIGURATION

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd7o9p97d9d6t&ycz^aennig5!65xv8g!ba!#cezu(*^&h0bv8!'

########## MEDIA CONFIGURATION
# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = normpath(join(DJANGO_ROOT, 'media'))

# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/media/'
MEDIA_UPLOAD_FOLDER = 'event_picture'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# Absolute path to the directory static files should be collected to. Don't put
# anything in this directory yourself; store your static files in apps' static/
# subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = normpath(join(DJANGO_ROOT, 'staticfiles'))

# URL prefix for static files.
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files.
STATICFILES_DIRS = (
    normpath(join(DJANGO_ROOT, 'static')),
)

# List of finder classes that know how to find static files in various
# locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
########## END STATIC FILE CONFIGURATION

########## TEMPLATE CONFIGURATION
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Directories to search when loading templates.
TEMPLATE_DIRS = (
    normpath(join(DJANGO_ROOT, 'web/templates')),
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.auth.context_processors.auth',
	'django.contrib.messages.context_processors.messages',
	'django.core.context_processors.request',
	'django.core.context_processors.media',
	'django.core.context_processors.request',
	'django.core.context_processors.static',
	'social.apps.django_app.context_processors.backends',
	'social.apps.django_app.context_processors.login_redirect'
)
########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
	'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',

)
########## END MIDDLEWARE CONFIGURATION


########## APP CONFIGURATION
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Point Django at the default FormPreview templates
    'django.contrib.formtools',

    # Admin panel and documentation.
    'django.contrib.admin',
    'django.contrib.admindocs',


    # South migration tool.
    'south',

    'rest_framework',
    # Celery task queue.
    #'djcelery',

    # django-social login
    'social.apps.django_app.default',
    # django-countries country listing
	'django_countries',
    # avatar handling
    'avatar',
    # support for tags
	'taggit',
    # a model field that can hold geoposition
    'geoposition',
    # a compressor for static files
    'compressor',
    # endless pagination
    'endless_pagination',

    # defined apps
    'web',
	'api',
	'mailer',

	#delete old Files and Images
	'django_cleanup'
)
########## END APP CONFIGURATION


########## URL CONFIGURATION
ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION

########## WSGI CONFIGURATION
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME
########## END WSGI CONFIGURATION

########## ATHENTICATION CONFIGURATION
AUTHENTICATION_BACKENDS = (
	'social.backends.github.GithubOAuth2',
	'social.backends.twitter.TwitterOAuth',
	'social.backends.facebook.FacebookOAuth2',
	'social.backends.facebook.FacebookAppOAuth2',
	'social.backends.google.GoogleOpenId',
	'django.contrib.auth.backends.ModelBackend',
)

AUTH_PROFILE_MODULE = 'api.UserProfile'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/login-error/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/'

SOCIAL_AUTH_ENABLED_BACKENDS = ('github', 'twitter', 'facebook', 'google')
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

SOCIAL_AUTH_GITHUB_KEY = ''
SOCIAL_AUTH_GITHUB_SECRET = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '...'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '...'
SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_TWITTER_KEY = ''
SOCIAL_AUTH_TWITTER_SECRET = ''
########## END ATHENTICATION CONFIGURATION

########## DJANGO-COUNTRIES CONFIGURATION
# Try to exclude all the countries not in EU

COUNTRIES_OVERRIDE = {
	u'AD': None,
	u'AE': None,
	u'AF': None,
	u'AG': None,
	u'AI': None,
	u'AL': None,
	u'AM': None,
	u'AO': None,
	u'AQ': None,
	u'AR': None,
	u'AS': None,
	u'AU': None,
	u'AW': None,
	u'AX': None,
	u'AZ': None,
	u'BA': None,
	u'BB': None,
	u'BD': None,
	u'BF': None,
	u'BH': None,
	u'BI': None,
	u'BJ': None,
	u'BL': None,
	u'BM': None,
	u'BN': None,
	u'BO': None,
	u'BQ': None,
	u'BR': None,
	u'BS': None,
	u'BT': None,
	u'BV': None,
	u'BW': None,
	u'BZ': None,
	u'CA': None,
	u'CC': None,
	u'CD': None,
	u'CF': None,
	u'CG': None,
	u'CI': None,
	u'CK': None,
	u'CL': None,
	u'CM': None,
	u'CN': None,
	u'CO': None,
	u'CR': None,
	u'CU': None,
	u'CV': None,
	u'CW': None,
	u'CX': None,
	u'DJ': None,
	u'DM': None,
	u'DO': None,
	u'DZ': None,
	u'EC': None,
	u'EG': None,
	u'EH': None,
	u'ER': None,
	u'ET': None,
	u'FJ': None,
	u'FK': None,
	u'FM': None,
	u'FO': None,
	u'GA': None,
	u'GD': None,
	u'GE': None,
	u'GF': None,
	u'GG': None,
	u'GH': None,
	u'GI': None,
	u'GL': None,
	u'GM': None,
	u'GN': None,
	u'GP': None,
	u'GQ': None,
	u'GS': None,
	u'GT': None,
	u'GU': None,
	u'GW': None,
	u'GY': None,
	u'HK': None,
	u'HM': None,
	u'HN': None,
	u'HT': None,
	u'ID': None,
	u'IL': None,
	u'IN': None,
	u'IO': None,
	u'IQ': None,
	u'IR': None,
	u'JE': None,
	u'JM': None,
	u'JO': None,
	u'JP': None,
	u'KE': None,
	u'KG': None,
	u'KH': None,
	u'KI': None,
	u'KM': None,
	u'KN': None,
	u'KP': None,
	u'KR': None,
	u'KW': None,
	u'KY': None,
	u'KZ': None,
	u'LA': None,
	u'LB': None,
	u'LC': None,
	u'LI': None,
	u'LK': None,
	u'LR': None,
	u'LS': None,
	u'LY': None,
	u'MA': None,
	u'MC': None,
	u'ME': None,
	u'MF': None,
	u'MG': None,
	u'MH': None,
	u'MK': None,
	u'ML': None,
	u'MM': None,
	u'MN': None,
	u'MO': None,
	u'MP': None,
	u'MQ': None,
	u'MR': None,
	u'MS': None,
	u'MU': None,
	u'MV': None,
	u'MW': None,
	u'MX': None,
	u'MY': None,
	u'MZ': None,
	u'NA': None,
	u'NC': None,
	u'NE': None,
	u'NF': None,
	u'NG': None,
	u'NI': None,
	u'NP': None,
	u'NR': None,
	u'NU': None,
	u'NZ': None,
	u'OM': None,
	u'PA': None,
	u'PE': None,
	u'PF': None,
	u'PG': None,
	u'PH': None,
	u'PK': None,
	u'PM': None,
	u'PN': None,
	u'PR': None,
	u'PS': None,
	u'PW': None,
	u'PY': None,
	u'QA': None,
	u'RE': None,
	u'RS': None,
	u'RU': None,
	u'RW': None,
	u'SA': None,
	u'SB': None,
	u'SC': None,
	u'SD': None,
	u'SG': None,
	u'SH': None,
	u'SJ': None,
	u'SL': None,
	u'SM': None,
	u'SN': None,
	u'SO': None,
	u'SR': None,
	u'SS': None,
	u'ST': None,
	u'SV': None,
	u'SX': None,
	u'SY': None,
	u'SZ': None,
	u'TC': None,
	u'TD': None,
	u'TF': None,
	u'TG': None,
	u'TH': None,
	u'TJ': None,
	u'TK': None,
	u'TL': None,
	u'TM': None,
	u'TN': None,
	u'TO': None,
	u'TT': None,
	u'TV': None,
	u'TW': None,
	u'TZ': None,
	u'UG': None,
	u'UM': None,
	u'US': None,
	u'UY': None,
	u'UZ': None,
	u'VA': None,
	u'VC': None,
	u'VE': None,
	u'VG': None,
	u'VI': None,
	u'VN': None,
	u'VU': None,
	u'WF': None,
	u'WS': None,
	u'YE': None,
	u'YT': None,
	u'ZA': None,
	u'ZM': None,
	u'ZW': None,
}
########## END ATHENTICATION CONFIGURATION


########## LOGGING CONFIGURATION
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

########## END LOGGING CONFIGURATION


########## GEOIP PATH
GEOIP_PATH = normpath(join(DJANGO_ROOT, 'geoip'))
########## END GEOIP PATH

########## DJANGO COMPRESSOR SETTINGS

COMPRESS_CSS_FILTERS = ('compressor.filters.cssmin.CSSMinFilter',)
COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'sass --scss {infile} {outfile}'),
)
########## END DJANGO COMRESSOR SETTINGS

########## PYTHON SOCIAL AUTH
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['first_name', 'last_name']


########## TESTING
TEST_RUNNER = 'django_pytest.test_runner.TestRunner'
SOUTH_TESTS_MIGRATE = True
########## END TESTING

CRISPY_TEMPLATE_PACK = 'bootstrap3'

try:
	from settings_local import *
except ImportError, e:
	pass

# if we're running on the server, use server specific settings
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
if ENVIRONMENT == 'production':
	from settings_production import *
