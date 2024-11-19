from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_approvel_system.settings')

app = Celery('credit_approvel_app')

# Use Django settings for configuration
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
