from app.tasks.celery import celery


@celery.task(name="periodic_task")
def periodic_task():
    print(12345)