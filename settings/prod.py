import os
from common import *
from aws import *
from tools.heroku import database_config

INSTALLED_APPS += (
    'storages',
)

DEBUG = TEMPLATE_DEBUG = False

DATABASES = {'default' : database_config() }

#Configure static content to be served form S3 
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
STATIC_URL = '//s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

#Email : using Amazon SES
EMAIL_BACKEND = 'django_ses.SESBackend'