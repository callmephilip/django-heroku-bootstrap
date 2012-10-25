# Django Heroku Bootstrap (DHB)

Get your Django app running on Heroku in less than 5 minutes. Really.

## What's in the box

Check out requirements.txt for details on the dependencies. 

DHB comes with an opinionated but powerful arsenal of tools that will help you take over the
world with your web app in no time 

* Amazon S3 for static content
* Amazon SES for emails
* Redis as a key-value store
* Celery for background tasks

All the settings are spread accross 3 files in the settings/ directory. 
* common.py has all your standard Django jazz that is identical for dev and production environments
* dev.py contains development specific settings 
* prod.py contains production specific settings and overrides

## Bootstrapping Your awesome app

1. Make sure you are logged in to Heroku
```
heroku login
```
2. Get a new git repository initialized
```
git init
```   
3. Create a new heroku project
```
heroku create
```
4. Being a smart developer you are using a virtual environment for your project. Activate it.
5. Run pip install -r requirements.txt. Grab a cup of tea/coffee. Come back to find all packages successfully installed.
6. Head to settings/prod.py and update your S3 credentials

### Static files

```python
#Your Amazon Web Services access key, as a string.
AWS_ACCESS_KEY_ID = ""

#Your Amazon Web Services secret access key, as a string.
AWS_SECRET_ACCESS_KEY = ""

#Your Amazon Web Services storage bucket name, as a string.
AWS_STORAGE_BUCKET_NAME = ""
```   

### Email

Assuming you've provided your AWS credentials in the settings file, email will just work. When running locally, emails will be dumped in the console. In production, DHB will send stuff through Amazon SES (make sure you use a verified sender address when sending emails with SES) 

```python
from django.core.mail import send_mail

send_mail('testing mail', 'Here is the message.', 'bob@mysite.com', ['bob@gmail.com'], fail_silently=False)
``` 

### Database please

Of course. You first need to get Postrgres on your Heroku 

```
heroku addons:add heroku-postgresql:dev
```

Now let's figure out the url for your database. To do this let's run the following command that comes wiht DHB

```
fab what_is_my_database_url
```

The output will look something like this

```
HEROKU_POSTGRESQL_<COLOR>_URL: postgres://<user>:<password>@<host>:5432/blabla
```

Use the first portion of the string (before ':') and  head to settings/prod.py to update your database url. Mine looks like this, for example

```python
DATABASES = {'default': dj_database_url.config(default=os.environ["HEROKU_POSTGRESQL_ROSE_URL"])}
```

### Redis

Vegetables are good for you. Especially when they help you build amazing apps. DHB uses Redis as a broker for Celery, which in turn is used for running background tasks. 

If you don't have Redis running on your dev machine, get it [here](http://redis.io/download).

Heroku offers an add-on called "Redis to go". Let's activate it    

```
heroku addons:add redistogo:nano
```

To see if it works

```python
import redis
import os

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis_instance = redis.from_url(redis_url)
redis_instance.set('answer', 42)
```

Once again, when running locally, make sure you have Redis server running on your machine.


### Celery

[Celery](http://celeryproject.org) allows you to run bacground tasks. DHB uses Celery coupled
with Redis. 


7. Run your site locally
```
fab run
```
8. Move all your static goodness to S3
```
fab collectstatic
``` 
9. Deploy to Heroku
```
git add .
```
```
git commit -a -m "first commit"
```
```
git push heroku master
```
10. Sync your data with Heroku
```
fab remote_syncdb
```
11. Make sure both web instance and the celeryd worker are up
```
heroku ps 
```
You should see both celeryd and web running. If celeryd is not there, run the following
```
heroku ps:scale celeryd=1
```