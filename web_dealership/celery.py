import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_dealership.settings")

app = Celery("web_dealership")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "generate_cars": {
        "task": "tasks.search_cars_to_dealership",
        "schedule": crontab(minute="*/1"),
    }
}
