from __future__ import absolute_import, unicode_literals

import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QnA_Platform.settings')

app = Celery('QnA_Platform')


app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {}

app.autodiscover_tasks()