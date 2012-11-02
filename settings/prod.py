import os
from common import *
from aws import *

INSTALLED_APPS += (
    'storages',
)

DEBUG = TEMPLATE_DEBUG = False

import dj_database_url

DATABASES = {'default' : dj_database_url.config() }  


#Configure static content to be served form S3 
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
STATIC_URL = '//s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

#Email : using Amazon SES
EMAIL_BACKEND = 'django_ses.SESBackend'