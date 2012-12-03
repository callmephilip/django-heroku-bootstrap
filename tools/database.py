import os
from functools import wraps
from fabric.api import local, settings


def needsdatabase(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        local("python manage.py syncdb --settings=settings.dev")
        return f(*args, **kwargs)
    return wrap

def remote_syncdb():
    local("heroku run python manage.py syncdb --settings=settings.prod")

def what_is_my_database_url():
    local("heroku config | grep POSTGRESQL")

def remote_migrate(app_name):
    if os.path.exists(os.path.join("./apps", app_name, "migrations")):
        with settings(warn_only=True):
            r = local("heroku run python manage.py migrate apps.%s --settings=settings.prod" % (app_name), capture=True)
            if r.find("django.db.utils.DatabaseError") != -1:
                print "Normal migration failed. Running a fake migration..."
                local("heroku run python manage.py migrate apps.%s --settings=settings.prod --fake" % (app_name))

def local_migrate(app_name):
    #TODO: figure out if there are actual models within the app
    if not os.path.exists(os.path.join("./apps", app_name, "models.py")):
        return

    if not os.path.exists(os.path.join("./apps", app_name, "migrations")):
        with settings(warn_only=True):
            r = local("python manage.py convert_to_south apps.%s --settings=settings.dev" % app_name, capture=True)
            if r.return_code != 0:
                return
    else:
        #app has been converted and ready to roll
        
        with settings(warn_only=True):
            r = local("python manage.py schemamigration apps.%s --auto --settings=settings.dev" % app_name)

            if r.return_code != 0:
                print "Scema migration return code != 0 -> nothing to migrate"
            else:
                local("python manage.py migrate apps.%s --settings=settings.dev" % (app_name))