import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "store.settings")

app = Celery("store")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "task1": {
        "task": "products.tasks.import_products",
        "schedule": crontab(hour="6", minute="00"),
    },
    "task2": {
        "task": "products.tasks.update_stock",
        "schedule": crontab(hour="8", minute="00"),
    },
}
