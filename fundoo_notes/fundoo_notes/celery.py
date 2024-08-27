'''
@Author: Vinit Gorakhnath Bhamare
@Date: 2024-08-16 13:58:30
@Last Modified by: Vinit Gorakhnath Bhamare
@Last Modified time: 2024-08-26 18:00:30
@Title : Fundoo Notes Celery
'''

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings


#changed
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fundoo_notes.settings')

app = Celery('fundoo_notes') 
app.conf.update(
    broker_connection_retry_on_startup=True,  # Maintain retry behavior on startup
    enable_utc=True,                         # Enable UTC for Celery
    timezone='ASIA/KOLKATA',                         # Set timezone to UTC
)
app.config_from_object('django.conf:settings', namespace='CELERY')

# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')