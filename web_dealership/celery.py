import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_dealership.settings')

app = Celery('web_dealership')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "search_car_to_dealership": {
        "task": "tasks.look_for_cars_for_dealership_by_model",
        "schedule": crontab(minute="*/2"),
    },
    "search_car_to_customer": {
        "task": "tasks.look_for_cars_for_customer_by_model",
        "schedule": crontab(minute="*/5"),
    }
}
