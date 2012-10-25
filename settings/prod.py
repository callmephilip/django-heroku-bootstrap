import os
from common import *


INSTALLED_APPS += (
    'storages',
)

DEBUG = TEMPLATE_DEBUG = False

import dj_database_url


# you will need to run this before to have Postgres on your server 
# heroku addons:add heroku-postgresql:dev

POSTGRES_URL = "HEROKU_POSTGRESQL_<COLOR>_URL"

if os.environ.has_key(POSTGRES_URL):
	DATABASES = {'default': dj_database_url.config(default=os.environ[POSTGRES_URL])}


# AWS settings

#Your Amazon Web Services access key, as a string.
AWS_ACCESS_KEY_ID = ""

#Your Amazon Web Services secret access key, as a string.
AWS_SECRET_ACCESS_KEY = ""

#Your Amazon Web Services storage bucket name, as a string.
AWS_STORAGE_BUCKET_NAME = ""

#Additional headers to pass to S3
AWS_HEADERS = {}

#Configure static content to be served form S3 
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
STATIC_URL = '//s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

#Email : using Amazon SES
EMAIL_BACKEND = 'django_ses.SESBackend'