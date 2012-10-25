web: gunicorn_django -b 0.0.0.0:$PORT -w 9 -k gevent --max-requests 250 --preload settings.prod
celeryd: python manage.py celeryd -E -B --loglevel=INFO --settings=settings.prod
celerybeat: python manage.py celerybeat -S djcelery.schedulers.DatabaseScheduler --settings=settings.prod