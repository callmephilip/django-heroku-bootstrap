from fabric.api import *
import os, sys


def patch_python_path(f):
	def wrap(*args, **kwargs):

		print "patching python path"

		if not os.environ.has_key("PYTHONPATH"):
			os.environ["PYTHONPATH"] = ""

		if not ('.' in os.environ["PYTHONPATH"].split(":")):
			print "adding . to the python path"			
			os.environ["PYTHONPATH"] = ".:%s" % os.environ["PYTHONPATH"] 

		return f(*args, **kwargs)
	return wrap

@patch_python_path
def deploy():
	print "Deploying your application"
	print "----------------------------"

	print "NOTE: We'll only deploy stuff that has been committed"

	print "Transferring static files to S3"
	collectstatic()	

	print "Pushing code on Heroku"
	local("git push heroku master")

	print "Syncing remote database"
	remote_migrate()

@patch_python_path
def run():
	print "Syncing database"
	local_migrate()
	local("foreman start -f Procfile.dev")

@patch_python_path
def syncdb():
    local("python manage.py syncdb --settings=%s.settings.dev" % figure_out_project_name()) 

def remote_syncdb():
    local("heroku run python manage.py syncdb --setting=settings.prod")

def what_is_my_database_url():
    local("heroku config | grep POSTGRESQL")

@patch_python_path
def collectstatic():
    local("python manage.py collectstatic --settings=settings.prod")

def __migrate(remote):

	apps_dir = "./apps"

	def enumerate_apps():
		return [ name for name in os.listdir(apps_dir) if os.path.isdir(os.path.join(apps_dir, name)) ]

	def app_has_models(app_name):
		return os.path.exists(os.path.join(apps_dir, app_name, "models.py"))

	apps = enumerate_apps()

	for app in apps:

		#don't attempt any migration related actions unless there are models associated with the app
		if not app_has_models(app):
			continue

		print "Checking migration situation for %s" % app

		if not os.path.exists(os.path.join(apps_dir,app,"migrations")):
			print "Running initial schema migration for %s" % app
			if remote:
				local("heroku run python manage.py schemamigration apps.%s --initial --settings=settings.prod" % (app))
			else:
				local("python manage.py schemamigration apps.%s --initial --settings=settings.dev" % (app))

		with settings(warn_only=True):
			print "Migrating %s ..." % app
			if remote:
				local("heroku run python manage.py migrate apps.%s --settings=settings.prod" % (app))
			else:
				local("python manage.py migrate apps.%s --settings=settings.dev" % (app))

@patch_python_path
def local_migrate():
	__migrate(False)

@patch_python_path
def remote_migrate():
	__migrate(True)