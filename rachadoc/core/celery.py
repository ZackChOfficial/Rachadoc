import os

from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

local_celery_app = Celery("core")
local_celery_app.config_from_object("django.conf:settings")
local_celery_app.conf.update(
    broker_url=settings.LOCAL_BROKER_URL,
    result_backend=settings.LOCAL_CELERY_RESULT_BACKEND,
    worker_send_task_events=True,
)

# Load task modules from all registered Django apps.
local_celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
