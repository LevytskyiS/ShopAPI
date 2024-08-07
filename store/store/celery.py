import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "store.settings")

app = Celery("store")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "task1": {
        "task": "products.tasks.import_products",
        "schedule": crontab(hour="6", minute="00"),
    },
    "task2": {
        "task": "products.tasks.update_stock",
        "schedule": crontab(hour="17", minute="16"),
    },
    # "task3": {
    #     "task": "products.tasks.import_prices",
    #     "schedule": crontab(hour="18", minute="34"),
    # },
}
