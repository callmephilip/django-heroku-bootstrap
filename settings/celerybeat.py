from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'runs-every-minute': {
        'task': 'apps.examples.tasks.report_errors',
        'schedule': timedelta(minutes=15)
    },
}

CELERY_TIMEZONE = 'UTC'