
import os
from datetime import datetime

import requests
from celery import Celery
from celery.schedules import crontab
# set the default Django settings module for the 'celery' program.
# from documentType.serializers import DocumentSerializer
from dirwatcher import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dirwatcher.settings')

# app = Celery('documentReminder')
app = Celery()

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print("Background task is up")

    sender.add_periodic_task(
        #Cron tab for more advanced usage
        # crontab(
        #    # hour=6,
        #    minute='*',# Executes every hour
        #    # minute='*',
        # ),
        10.0,
        test.s('DIR CHECKER'),
    )

@app.task
def test(arg):
    import winsound
    winsound.Beep(2000, 500)

    #Method 1 - make a server request - Not a good approach, i have done this as a part of testing
    # url = "http://127.0.0.1:80/dir/?path=all"
    # requests.get(url)

    # Method 2 - By function call
    from dirRecord.views import dirMonitorChecker
    dirMonitorChecker('all','')

    print("Directory check up completed : "+arg)
