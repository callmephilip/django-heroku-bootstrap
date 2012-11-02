from fabric.api import *
import os

def init():
	print "Initializing your django app"
	print "----------------------------"

	print "Installing dependencies locally (might take a while)..."

	local("sudo pip install -r requirements.txt")

	print "Pick a name for your heroku app"
	
	app_name = raw_input()
	local("heroku login")
	local("heroku create %s" % app_name)

	print "Adding PostgresSQL to Heroku"
	local("heroku addons:add heroku-postgresql:dev")

	print "Adding RedisToGo to Heroku"
	local("heroku addons:add redistogo:nano")

	print "Syncing code with heroku"

	local("git add .")
	local("git commit -a -m 'initial app bootstrap'")
	local("git push heroku master")

	print "Syncing with remote database"

	remote_syncdb()

	print "Transferring static files to Amazon"

	collectstatic()

	print "Done. Your app is bootstrapped and ready to go"

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

def run():
	print "Syncing database"
	local_migrate()
	local("foreman start -f Procfile.dev")

def syncdb():
    local("python manage.py syncdb --settings=settings.dev") 

def remote_syncdb():
    local("heroku run python manage.py syncdb --setting=settings.prod")

def what_is_my_database_url():
    local("heroku config | grep POSTGRESQL")

def collectstatic():
    local("python manage.py collectstatic --settings=settings.prod")

def __migrate(remote):

	apps_dir = "./apps"

	def enumerate_apps():
		return [ name for name in os.listdir(apps_dir) if os.path.isdir(os.path.join(apps_dir, name)) ]

	apps = enumerate_apps()

	for app in apps:
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

def local_migrate():
	__migrate(False)

def remote_migrate():
	__migrate(True)