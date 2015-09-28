from .settings import *
import os
import dj_database_url

DEBUG = False

ADMINS = (
    ('Codeweek', 'europecodes@gmail.com'),
)

dbconfig = dj_database_url.config()
if dbconfig:
    DATABASES['default'] = dbconfig
else:
    del DATABASES['default']

SECRET_KEY = os.environ.get('SECRET_KEY', '')

STATIC_URL = '/static/'
STATIC_ROOT = join(DJANGO_ROOT, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(DJANGO_ROOT, 'static'),
)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# S3 Storage settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# use http instead of https
AWS_S3_SECURE_URLS = False
# don't add complex authentication-related query parameters for requests
AWS_QUERYSTRING_AUTH = False
# Read secret data for social logins
AWS_S3_ACCESS_KEY_ID = os.environ.get('AWS_S3_KEY', '')
AWS_S3_SECRET_ACCESS_KEY = os.environ.get('AWS_S3_SECRET', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_BUCKET', '')

# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/'

# Get secret data for social logins
SOCIAL_AUTH_GITHUB_KEY = os.environ.get('GITHUB_KEY', '')
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get('GITHUB_SECRET', '')
SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('FACEBOOK_KEY', '')
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('FACEBOOK_SECRET', '')
SOCIAL_AUTH_TWITTER_KEY = os.environ.get('TWITTER_KEY', '')
SOCIAL_AUTH_TWITTER_SECRET = os.environ.get('TWITTER_SECRET', '')
