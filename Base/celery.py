# from __future__ import absolute_import, unicode_literals
# from celery import Celery


# app = Celery('Base')

# # Load configuration from settings.py
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Auto-discover tasks in all installed apps
# app.autodiscover_tasks()

# celery -A your_project worker --loglevel=info
# celery -A your_project beat --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach
