from fabric.api import *


def run():
    local("foreman start -f Procfile.dev")

def syncdb():
    local("python manage.py syncdb --settings=settings.dev") 

def remote_syncdb():
    local("heroku run python manage.py syncdb --setting=settings.prod")

def what_is_my_database_url():
    local("heroku config | grep POSTGRESQL")

def collectstatic():
    local("python manage.py collectstatic --settings=settings.prod")

