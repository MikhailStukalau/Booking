from celery import Celery
from app.config import settings
from celery.schedules import crontab


celery = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=[
        "app.tasks.tasks",
        "app.tasks.scheduled",
    ]
)

celery.conf.beat_schedule = {
    "tasks_sett": {
        "task": "periodic_task",
        "schedule": 10, #seconds
        # "schedule": crontab(minute="30", hour="15")
    }
}