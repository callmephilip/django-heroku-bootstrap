from fabric.api import *


def run():
    local("foreman start -f Procfile.dev")

def syncdb():
    local("python manage.py syncdb --settings=settings.dev") 

def collectstatic():
    local("python manage.py collectstatic --settings=settings.prod")

