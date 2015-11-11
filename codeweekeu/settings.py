"""
Django settings for codeweekeu project.
"""

import sys
import os
from os.path import abspath, basename, dirname, join, normpath

# PATH CONFIGURATION
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
# END PATH CONFIGURATION

# DEBUG CONFIGURATION
# Disable debugging by default.
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# END DEBUG CONFIGURATION

# MANAGER CONFIGURATION
# Admin and managers for this project. These people receive private site
# alerts.
ADMINS = (
    ('Errors', 'errors@codeweek.eu'),
)

MANAGERS = ADMINS
# END MANAGER CONFIGURATION

# DATABASE CONFIGURATION
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
# END DATABASE CONFIGURATION

ALLOWED_HOSTS = ['localhost', 'codeweek.eu']
# GENERAL CONFIGURATION
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

# Dummy function, so that "makemessages" can find strings which should be
# translated.
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
# END GENERAL CONFIGURATION

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd7o9p97d9d6t&ycz^aennig5!65xv8g!ba!#cezu(*^&h0bv8!'

# MEDIA CONFIGURATION
# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = normpath(join(DJANGO_ROOT, 'media'))

# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/media/'
MEDIA_UPLOAD_FOLDER = 'event_picture'
# END MEDIA CONFIGURATION


# STATIC FILE CONFIGURATION
# Absolute path to the directory static files should be collected to. Don't put
# anything in this directory yourself; store your static files in apps' static/
# subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = normpath(join(DJANGO_ROOT, 'staticfiles'))

# URL prefix for static files.
STATIC_URL = '/static/'

# The base URL where to fetch the CSS, JS and image files for the header and
# footer design. It should point to the URL of the static codeweek.eu website.
# Make sure this URL ends with a slash: /
THEME_ASSETS_BASE_URL = 'http://codeweek.eu/'

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
# END STATIC FILE CONFIGURATION

# TEMPLATE CONFIGURATION
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
    'social.apps.django_app.context_processors.login_redirect',
    'django_settings_export.settings_export',
)
# END TEMPLATE CONFIGURATION

# Cache configuration
CACHE_MIDDLEWARE_ALIAS='default'
CACHE_MIDDLEWARE_SECONDS=120
CACHE_MIDDLEWARE_KEY_PREFIX=''

# MIDDLEWARE CONFIGURATION
MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',

)
# END MIDDLEWARE CONFIGURATION


# APP CONFIGURATION
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
    'rest_framework_extensions',
    # Celery task queue.
    #'djcelery',

    # django-social login
    'social.apps.django_app.default',
    # django-countries country listing
    'django_countries',
    # additional info about countries
    'countries_plus',
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
    # Django admin import/export functionality for resources
    'import_export',

    # defined apps
    'web',
    'api',
    'mailer',

    # delete old Files and Images
    'django_cleanup',

    # patches
    'patches',
)
# END APP CONFIGURATION


# URL CONFIGURATION
ROOT_URLCONF = '%s.urls' % SITE_NAME
# END URL CONFIGURATION

# WSGI CONFIGURATION
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME
# END WSGI CONFIGURATION

# ATHENTICATION CONFIGURATION
AUTHENTICATION_BACKENDS = (
    'social.backends.github.GithubOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.google.GoogleOAuth2',
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
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''
SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_TWITTER_KEY = ''
SOCIAL_AUTH_TWITTER_SECRET = ''
# END ATHENTICATION CONFIGURATION

# DJANGO-COUNTRIES CONFIGURATION
# This was used in the past to exclude countries not in Europe
COUNTRIES_OVERRIDE = {
    # Don't include Antarctica
    'AQ': None,
    'TW': _('Taiwan'),
}

# END ATHENTICATION CONFIGURATION

# LOGGING CONFIGURATION
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

# END LOGGING CONFIGURATION


# GEOIP PATH
GEOIP_PATH = normpath(join(DJANGO_ROOT, 'geoip'))
# END GEOIP PATH

# DJANGO COMPRESSOR SETTINGS

COMPRESS_CSS_FILTERS = ('compressor.filters.cssmin.CSSMinFilter',)
COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'sass --scss {infile} {outfile}'),
)
# END DJANGO COMRESSOR SETTINGS

# PYTHON SOCIAL AUTH
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['first_name', 'last_name']


# TESTING
TEST_RUNNER = 'django_pytest.test_runner.TestRunner'
SOUTH_TESTS_MIGRATE = True
# END TESTING

CRISPY_TEMPLATE_PACK = 'bootstrap3'

SETTINGS_EXPORT = [
    'THEME_ASSETS_BASE_URL',
]


# Settings for sending evnet organizers reminder emails to submit an evnet
# report and claim their certificate.
EVENT_REPORT_REMINDERS_FROM_EMAIL = 'info@codeweek.eu'

# The notification script runs each hour. The SendGrid free account has
# a limit of 400 emails per day.
EVENT_REPORT_REMINDER_EMAILS_PER_HOUR = 16

# Send at most X reminders for event reporting.
# Set to 0 to disable reminding for event reporting.
EVENT_REPORT_REMINDERS_LIMIT = 3

# If we're allowed to send more than one reminder email, reminders
# will be sent each X days.
EVENT_REPORT_REMINDERS_INTERVAL_IN_DAYS = 21


try:
    from settings_local import *
except ImportError as e:
    pass

# if we're running on the server, use server specific settings
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
if ENVIRONMENT == 'production':
    try:
        from settings_production import *
    except ImportError as e:
        pass
