from fabric.api import *
from functools import wraps
import os, sys

__all__ = ['deploy','run','collectstatic']

def patch_python_path(f):
	@wraps(f)	 	
	def wrap(*args, **kwargs):
		ROOT = os.pathsep.join([os.path.abspath(os.path.dirname(__file__))])

		if not os.environ.has_key("PYTHONPATH"):
			os.environ["PYTHONPATH"] = ""

		if not (ROOT in os.environ["PYTHONPATH"].split(":")):
			os.environ["PYTHONPATH"] = "%s:%s" % (os.environ["PYTHONPATH"], ROOT)

		if not ROOT in sys.path:
			sys.path.append(ROOT)

		return f(*args, **kwargs)
	return wrap

@patch_python_path
def deploy():
	from tools.git import check_git_state, is_git_clean
	from tools.database import needsdatabase, local_migrate, remote_migrate, remote_syncdb
	from tools.apps import enumerate_apps

	@check_git_state
	@needsdatabase
	def __deploy():
		print "Deploying your application"
		print "----------------------------"

		print "Migrations..."

		for app in enumerate_apps():
			local_migrate(app)
			
		if is_git_clean():
			print "Pushing code on Heroku"
			local("git push heroku master")
		else:
			print "Committing migrations..."
			local("git add .")
			local("git commit -a -m '[DHB] data migrations'")


		print "Sync remote database"
		remote_syncdb()


		for app in ["djcelery"]:
			with settings(warn_only=True):
				print "Migrating %s ..." % app
				local("heroku run python manage.py migrate %s --settings=settings.prod" % (app))

		for app in enumerate_apps():
			remote_migrate(app)

		print "Transferring static files to S3"
		collectstatic()	

	__deploy()

@patch_python_path
def run():
	print sys.path

	from tools.database import needsdatabase, local_migrate
	from tools.apps import enumerate_apps
	from tools.heroku import start_foreman

	@needsdatabase
	def __run():
		for app in ["djcelery"]:
			with settings(warn_only=True):
				print "Migrating %s ..." % app
				local("python manage.py migrate %s --settings=settings.dev" % (app))
				
		for app in enumerate_apps():
			with settings(warn_only=True):
				local_migrate(app)

		start_foreman()		

	__run()

@patch_python_path
def collectstatic():
    local("python manage.py collectstatic --noinput --settings=settings.static")