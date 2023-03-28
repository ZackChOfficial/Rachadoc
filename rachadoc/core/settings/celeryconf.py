from . import env

LOCAL_BROKER_URL = env("LOCAL_BROKER_URL")
LOCAL_CELERY_RESULT_BACKEND = env("LOCAL_CELERY_RESULT_BACKEND")
CELERY_DEFAULT_QUEUE = "celery_local_task_worker"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
