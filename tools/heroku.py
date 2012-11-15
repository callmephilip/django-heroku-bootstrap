import os, re
import dj_database_url
from fabric.api import local, settings

def start_foreman(proc_file="Procfile.dev"):
    local("foreman start -f %s" % proc_file)

def database_config(env_varibale_pattern="HEROKU_POSTGRESQL_\S+_URL", default_env_variable="DATABASE_URL"):

    r = re.compile(env_varibale_pattern)

    urls = filter(lambda k : r.match(k) is not None, os.environ.keys())

    if len(urls) > 1:
        if not os.environ.has_key(default_env_variable):
            print "Multiple env variables matching %s detected. Using %s" % (env_varibale_pattern, urls[0])


    if len(urls) == 0:
        if not os.environ.has_key(default_env_variable):
            raise Exception("No database detected. Make sure you enable database on your heroku instance (e.g. heroku addons:add heroku-postgresql:dev)")

    return dj_database_url.config(default_env_variable, os.environ[urls[0]] if len(urls) !=0 else None)
